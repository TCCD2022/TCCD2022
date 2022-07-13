# from django.shortcuts import render

# Create your views here.

# pages/views.py
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import TemplateView, ListView, View
# from django.db.models import F
from datafiles.models import Datafile, Column, Analysis, Method, Analysis_results, Analysis_on_columns
from datafiles.forms import DataModelForm
from django.utils import timezone

import os.path
import requests
import json
# from datetime import datetime

class HomePageView(TemplateView):
    
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DataModelForm()
        if self.request.user.is_authenticated:
            current_user = self.request.user
            context['documents'] = Datafile.objects.filter(user_id=current_user)
            col_dic = {}
            for file in context['documents']:
                col_dic.update({file.id: Column.objects.filter(datafile=file.id)})
            context['cols']=col_dic
            print(col_dic)
            context['form'] = form
        return context
    
    def post(self, request, *args, **kwargs):
        current_user = request.user
        form = DataModelForm(request.POST, request.FILES)
        if request.method == 'POST':
            if form.is_valid():
                newdoc = Datafile(docfile = request.FILES['docfile'])
                newdoc.user = current_user
                newdoc.save()
                return HttpResponseRedirect(reverse('home'))
        return render(request, 'home.html', {'form': form})

class ListMethodsView(View):
    
    def get(self, request, *args, **kwargs):
        print('List methods view Url found')
        results = Method.objects.all().values('id','name','json_schema','doc_file')
        return JsonResponse({"results":list(results)})

class RunMethodView(View):
    '''
    Executed the selected method
    '''
    def post(self, request, *args, **kwargs):
        print('Run method view Url found')
        # print(request.POST.get('values'))
        params = request.POST.get('values')
        params = json.loads(params)
        file_record = Datafile.objects.get(pk=params["fileid"])
        print(json.dumps(params,indent=4))
        if file_record:
            # fname = file_record.docfile.name
            used_method = Method.objects.get(pk=int(params["methodid"]))

            # take initial time

            start_time = timezone.now() # datetime.now()
            new_analysis = Analysis(user=self.request.user, start_time = start_time,
                                    datafile = file_record,
                                    method = used_method, # extract metadata
                                    # end_time = None,
                                    status = 'W'
            )

            # print(new_analysis)
            new_analysis.save()
            # call plumber api
            r = requests.post(used_method.url_service,
                              data = {'metadata':request.POST.get('values')}
            )

            if r.ok:
                end_time = timezone.now() # datetime.now()
                y = json.loads(r.text)
                print(y)
                if 'error' in y:
                    return JsonResponse(y)
                print(y['pdffile'][0])
                print(y['format'][0])
                new_analysis.end_time = end_time

                # cols = Column.objects.filter(datafile=file_record)
                # print(cols)
                for col in params["col_ids"]:
                    print(col['colname'])
                    colrec = Column.objects.get(pk=int(col['colid']))
                    new_ac = Analysis_on_columns(column_id=colrec,analysis_id=new_analysis,
                                                 dependent=False)
                    new_ac.save()

                # TODO: consider more than on file as results
                new_result = Analysis_results(analysis_id = new_analysis,
                                              file_format=y['format'][0],
                                              file_path=y['pdffile'][0]

                )

                new_result.save()

                new_analysis.status = 'C'
                params.pop("fileid")
                params.pop("filename")
                params.pop("col_ids")
                params.pop("methodid")
                new_analysis.parameters = params
                print(new_analysis)
                new_analysis.save()

                return JsonResponse({"results":[{"id":new_result.id,"file_path": y['pdffile'][0]}]})
                # return JsonResponse({"results":[{"file_path": y['pdffile'][0]}]})
            else:

                return JsonResponse({'error': str(r.status_code) + " " + r.reason})
        else:
            return JsonResponse({'error': 'File not found'})

#        return JsonResponse({"results":"URL run method found"})
    
class ColumnsView(ListView):
    model = Column
    context_object_name = 'column_list'
    template_name = 'home.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     current_user = self.request.user
    #     context['documents'] = Datafile.objects.filter(user_id=current_user)
    #     return context

class ExtractMetadataView(View):
    '''Extract filesize, number of rows and columns
    '''

    def get(self, request,*args,**kwargs):
        # pk is defined to in pages/urls.py
        docid = kwargs["pk"]
        print(docid)
        if self.request.user.is_authenticated:
            file_record = Datafile.objects.get(pk=docid)
            if file_record:

                fname = file_record.docfile.name
                fformat = file_record.file_format

                used_method = Method.objects.get(pk=1)
                # take initial time
                start_time = timezone.now() #datetime.now()
                new_analysis = Analysis(user=self.request.user, start_time = start_time, datafile = file_record,
                                        method = used_method, # extract metadata
                                        # end_time = None,
                                        status = 'W'
                )                
                
                if fformat == None:
                    # TODO: rollback in case part of the procedure fails
                    _, extension = os.path.splitext(fname)
                    extension = extension[1:].upper()
                    find_ext = [item for item in Datafile.FFORMAT if item[0] == extension]
                    # Check if the file format is supported
                    if not find_ext:
                        extension = 'UNS'
                        file_record.file_format = extension
                        file_record.supported = False
                        file_record.save()
                        # take end time
                        end_time = timezone.now() 
                        # Analysis
                        new_analysis.end_time = end_time
                        new_analysis.status = 'C'
                        new_analysis.save()
                        return JsonResponse({"error":'FORMAT OF THE ' + fname + ' FILE IS NOT SUPPORTED'})
                    else:
                        # call plumber api
                        r = requests.post('http://plumber:8181/coltypes',
                                  data = {'filename':'/code/media/' + fname})
                        # print(dir(r))
                        print(r.text)
                        if r.ok:
                            y = json.loads(r.text)
                            # y = json.loads(y[0])
                            cols = y["coltypes"][0]
                            print(y["numrows"])
                            print(y["numcols"])
                            print(type(cols),cols)

                            # Store table properties
                            file_record.num_rows = y["numrows"][0]
                            file_record.num_cols = y["numcols"][0]
                            file_record.filesize = y["filesize"][0]
                            file_record.supported = True
                            file_record.file_format = find_ext
                            file_record.save()

                            # Store found columns
                            colattrs = {}
                            for var, coltype in cols.items():
                                print(var," ",coltype)
                                match coltype:
                                    case "double":
                                        dbcoltype = "DB"
                                        dbscale = "CT"
                                    case "logical":
                                        dbcoltype = "BL"
                                        dbscale = "NM"
                                    case "integer":
                                        dbcoltype = "IN"
                                        dbscale = "DS"
                                    case "character":
                                        dbcoltype = "ST"
                                        dbscale = "NM"
                                    case _:
                                        dbcoltype = "UK"
                                        dbscale = None
                                
                                new_col = Column(datafile = file_record, name= var, col_type = dbcoltype, scale = dbscale)
                                # TODO: Think on different column ids to prevent collisions 
                                new_col.save()
                                colattrs[var] = {'id':new_col.id,'type':new_col.get_col_type_display(),'scale':new_col.get_scale_display(),
                                                 'vis-col-url': new_col.get_find_col_vis_url()
                                                 # ,'create-col-vis-url' : new_col.get_create_vis_col_url()
                                }
                            print(colattrs)

                            # Store Analysis,
                            end_time = timezone.now()
                            new_analysis.end_time = end_time
                            new_analysis.status = 'C'
                            new_analysis.save()                            

                            # Store Files - Columns relationship
                            y["supported"] = file_record.supported
                            y["colurl"] = colattrs
                            return JsonResponse(y)
                        else:
                            return JsonResponse({"error":'Error during file processing (To be added ERROR code)'})
                else:
                    print('Metadata already exists')
                    return JsonResponse({"result":'Metadata already exists'})
            else:
                return JsonResponse({"error":'File record not found'})
        else:
            return JsonResponse({"error":'User not authenticated'})

# class CreateVisColumnView(View):
#     '''
#     Visualize a column as distributions and/or boxplots

#     TODO: verify that the plot does not exist, otherwise the plot will
#     be replaced and a new analysis will be registered

#     '''
#     def post(self, request, *args, **kwargs):
#         docid = kwargs["pk"]
#         colid = kwargs["id"]
#         file_record = Datafile.objects.get(pk=docid)
#         column_record = Column.objects.get(pk=colid)
#         if file_record and column_record:
#             fname = file_record.docfile.name
#             cname = column_record.name
#             used_method = Method.objects.get(pk=2)

#             results = Analysis_results.objects.filter(analysis_id__on_cols=column_record,
#                                                       analysis_id__method=used_method).values('id','file_path')
#             l = len(results)
#             if l > 0:
#                 print("Vio-vox vis exists:", results[0]['file_path'])
#                 return JsonResponse({"results":list(results)})
#             else:        
#                 print("Vio-box plot will be created ",fname,cname)
#                 # take initial time
#                 start_time = timezone.now() # datetime.now()
#                 new_analysis = Analysis(user=self.request.user, start_time = start_time,
#                                         datafile = file_record,
#                                         method = used_method, # extract metadata
#                                         # end_time = None,
#                                         status = 'W'
#                 )
#                 new_analysis.save()

#                 # call plumber api
#                 r = requests.post('http://plumber:8181/'+used_method.end_point,
#                                   data = {'filename':'/code/media/' + fname,
#                                           'columns':[cname]},
#                 )
                
#                 if r.ok:
#                     end_time = timezone.now() # datetime.now()
#                     y = json.loads(r.text)
#                     print(y)
#                     print(y['pdffile'][0])
#                     print(y['format'][0])
#                     new_analysis.end_time = end_time
#                     new_analysis.status = 'C'
#                     new_analysis.save()
#                     new_ac = Analysis_on_columns(column_id=column_record,analysis_id=new_analysis,
#                                                  dependent=False)
#                     new_ac.save()
#                     new_result = Analysis_results(analysis_id = new_analysis,
#                                                   file_format=y['format'][0],
#                                                   file_path=y['pdffile'][0]
#                     )
#                     new_result.save()

#                     return  JsonResponse({"results":[{"id":new_result.id,"file_path": y['pdffile'][0]}]})
#                 else:
#                     return  JsonResponse({"results":r.status_code + " " + r.reason})
#         else:
#             return JsonResponse({"results":'File not found'})

class FindColVisView(View):
    '''
    Find visualizations of a column
    '''
    def get(self, request,*args,**kwargs):
        docid = kwargs["pk"]
        colid = kwargs["id"]
        col_record = Column.objects.get(pk=colid)
        print(docid,colid)
        # results = Analysis_results.objects.filter(analysis_id__on_cols=col_record,
        #                              analysis_id__method=metodo).values('id',text = F('file_path'))
        results = Analysis_results.objects.filter(analysis_id__on_cols=col_record).values('id','file_path')

        for result in results:
            print(result)
        return JsonResponse({"results":list(results)})
        # pk is defined to in pages/urls.py

# class CreateFileDistView(View):
#     '''
#     Create overlapped violin and box plots using the columns in a datafile

#     '''
#     def post(self, request, *args, **kwargs):
#         docid = kwargs["pk"]
#         file_record = Datafile.objects.get(pk=docid)
#         if file_record:
#             fname = file_record.docfile.name
#             used_method = Method.objects.get(pk=3)

#             prev_result = Analysis.objects.filter(datafile=docid,method=used_method.pk)

#             ## prev_result.delete()
#             print("Previous results length:",len(prev_result))

#             if prev_result:
#                 print('The file has been processed before',prev_result)
#                 # {"results":[{"id":new_result.id,"file_path": y['pdffile'][0]}]}
#                 return  JsonResponse(prev_result[0])
#             else:
#                 # take initial time
#                 start_time = timezone.now() # datetime.now()
#                 new_analysis = Analysis(user=self.request.user, start_time = start_time,
#                                         datafile = file_record,
#                                         method = used_method, # extract metadata
#                                         # end_time = None,
#                                         status = 'W'
#                 )
#                 new_analysis.save()

#                 # call plumber api
#                 r = requests.post('http://plumber:8181/'+used_method.end_point,
#                                   data = {'filename':'/code/media/' + fname,
#                                           'columns':[]},
#                 )

#                 if r.ok:
#                     end_time = timezone.now() # datetime.now()
#                     y = json.loads(r.text)
#                     print(y)
#                     print(y['pdffile'][0])
#                     print(y['format'][0])
#                     new_analysis.end_time = end_time
#                     new_analysis.status = 'C'
#                     print(new_analysis)
#                     new_analysis.save()
                    
#                     cols = Column.objects.filter(datafile=file_record)
#                     print(cols)
#                     for col in cols:
#                         print(col.name)
#                         new_ac = Analysis_on_columns(column_id=col,analysis_id=new_analysis,
#                                                      dependent=False)
#                         new_ac.save()

#                     new_result = Analysis_results(analysis_id = new_analysis,
#                                                   file_format=y['format'][0],
#                                                   file_path=y['pdffile'][0]
#                     )
#                     new_result.save()
#                     return JsonResponse({"results":[{"id":new_result.id,"file_path": y['pdffile'][0]}]})
#                 else:
#                     return JsonResponse({'error': r.status_code + " " + r.reason})
#         else:
#             return JsonResponse({'error': 'File not found'})
    
    
        
class FindFileResultsView(View):
    '''
    Find results of a datafile
    '''
    def get(self, request,*args,**kwargs):
        docid = kwargs["pk"]
        # results = Analysis_results.objects.filter(analysis_id__datafile=docid).values('id',text = F('file_path'))
        results = Analysis_results.objects.filter(analysis_id__datafile=docid).values('id','file_path')
        for result in results:
            print(result)
        # return HttpResponse('The url has been found')
        return JsonResponse({"results":list(results)})
        
class AboutPageView(TemplateView): # new
    template_name = 'about.html'

class CleanMetadataView(View):
    '''
    Clean metadata from a file record
    '''   

    def post(self, request, *args, **kwargs):
        current_user = request.user
        docid = kwargs["pk"]
        if request.method == 'POST':
            if self.request.user.is_authenticated:
                file_record = Datafile.objects.get(pk=docid)
                if file_record:
                    file_cols = Column.objects.filter(datafile_id=docid)
                    print("File columns ",file_cols, docid)
                    file_cols.delete()
                            # delete table properties
                    file_record.num_rows = None
                    file_record.num_cols = None
                    file_record.filesize = None
                    file_record.supported = None
                    file_record.file_format = None
                    file_record.save()
                    return JsonResponse({'result':'File metadata deleted'})
                else:
                    return JsonResponse({'result':'Record not found'})
            else:
                return JsonResponse({'result':'User not autheticated'})
        else:
            return JsonResponse({'result':'Method not allowed'})


# class CreateNetworkView(View):
#     '''
#     Create pairwise relationship visualization
#     TODO: implement the call

#     {
# 	"model": "datafiles.Method",
# 	"fields": {
# 	    "id": 4,
# 	    "name" : "Pairwise network relationship",
# 	    "description" : "",
# 	    "prog_language" : "R",
# 	    "end_point" : "/create_network"
# 	}
#     }

#     '''   

#     def post(self, request, *args, **kwargs):
#         print('Create network view Url found')
#         return JsonResponse({"results":"url create network found"})
