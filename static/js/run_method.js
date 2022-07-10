$( function() {
    var dialog, form;
	// From http://www.whatwg.org/specs/web-apps/current-work/multipage/states-of-the-type-attribute.html#e-mail-state-%28type=email%29

    function submitJob() {
	var validated = $('#runmform').jsonForm().validate();
      }
      
    function formulario(data,fileid, filename, listcolids, methodid){
	// console.log(data);
	// var t = JSON.parse(data);
	var tform = data;
       $('#runmform').jsonForm({
           "schema":tform,
	   "form": [
	       "*",
	       {
		   "type": "actions",
		   "items": [
		       {
		       	   "type": "submit",
		       	   "title": "Submit",
		       },
		       {
			   "type": "button",
			   "title": "Cancel",
			   "onClick": function (evt) {
		               evt.preventDefault();
			       dialog.dialog( "close" );
			       // alert('Thank you!'); 	       
			   }
		       }
		   ]
	       }
	   ],
           "onSubmit":  function (errors, values) {
	       if (errors) {
		   console.log(errors)
               }
	       else {
		   values.fileid = fileid;
		   values.filename = filename;
		   values.col_ids = listcolids;
		   values.methodid = methodid;
		   let url3 = "runmethod/" + values.methodid;
		   $.ajax({
		       url:url3,
		       dataType: "json",
		       type:"POST",
		       data: { csrfmiddlewaretoken: getCookie('csrftoken'),
			       'values':JSON.stringify(values)},
		       success: function(result){
			   var $iframe = $('#panel-res');
			   $( ".results_list" ).empty();
			   if (result.results.length > 0) {
			       $iframe.attr('src',result.results[0].file_path.slice(5));
			       result.results[0].selected = true;
			       for (var i = 0; i <  result.results.length; i++) {
				   result.results[i].text = result.results[i].file_path.split('/').pop();
		   		   console.log(result.results[i]);
			       }
			       $( ".results_list" ).select2({
				   //tokenSeparators: [",", " "],
				   allowClear: true,
				   placeholder: "Select result",
				   data: result.results
			       });		
			       console.log(result)
			   }
			   // TODO: verify that all variables are removed
			   dialog.dialog( "close" );
		       },
		       error:function(error){
   			   // alert(error)
 			   console.log(`Error "${error}"`) || alert(error)
		       }
		   });
	       }
	   }
       });
    }

    dialog = $( "#run-method-form" ).dialog({
      autoOpen: false,
      height: 400,
      width: 350,
      modal: true,
      // buttons: {
      //   "Submit job": submitJob,
      //   Cancel: function() {
      //     dialog.dialog( "close" );
      //   }
      // },
      close: function() {
        form[ 0 ].reset();
      //  allFields.removeClass( "ui-state-error" );
      }
    });
 
    form = dialog.find( "form" ).on( "submit", function( event ) {
      event.preventDefault();
      // addUser();
    });
 
    $( "#runmethod" ).button().on( "click", function() {
	var dfile = $(".selected")
	var dmethod = $("#fc_method").select2('data')
	var mid = dmethod[0].id
	if (dfile.length && mid){
	    var label = $("#proc_file")
	    label.text(dfile.text())

	    let schemafile = dmethod[0].json_schema;
	    console.log(dfile[0].id);
	    var c = dfile.siblings().first();

	    console.log(c)
	    
	    if (c) {
		// $('#dcolumns .dlist').empty();
		var colids = [];
		c.find('input[type="checkbox"]:checked').each(function() {
		    //$('#dcolumns .dlist').append('<li>'+$(this).val()+'</li>')
		    let t = $(this).next()[0].title;
		    const typescale = t.split(", ");
		    colids.push({"colid":$(this)[0].id, "colname":$(this).val(),
				 "type":typescale[0],"scale":typescale[1]});
		});
		if (!colids.length) {
		    c.find('input[type="checkbox"]').each(function() {
			let t = $(this).next()[0].title;
			const typescale = t.split(", ");
			colids.push({"colid":$(this)[0].id, "colname":$(this).val(),
				     "type":typescale[0],
				     "scale":typescale[1]});

		    });    
		}
		if (!colids.length) {
		    alert("No columns found\nTry to run the 'Extract metadata' method\n" +
			  "Check that the file is supported by hovering on the file name\n"+
                           "Finally, try running the method again");
		    return; 
		}
		$('#runmform').empty();
		fetch(schemafile)
		    .then(response => response.text())
		    .then(
			function (data) {
			    let fname = dfile.text();
			    fname = fname.replace(/\s/g, '');
			    let fileid = dfile[0].id;
			    var t = JSON.parse(data);

			    $.each(t.properties, function(key, value) {
			    	if ('enum' in value){
			    	    if (value['enum'].includes('--No variable--')){
					// add column names
					colids.forEach(function(element){
					    value['enum'].push(element.colname);
					    console.log(element.colname);
					});
			    	    }
			    	}
			    });
			    
			    formulario(t, fileid, fname, colids, mid);
			}
		    );

		dialog.dialog( "open" );
	    }
	    else {
		alert("No columns found (perhaps extract metadata)")
	    }
	}
	else {
	    alert("Please select a data file and a method")
	}
    });
});



$('.methods_list').on('select2:select', function (e) {
    var data = e.params.data;
    var $iframe = $('#panel-res');

    $iframe.attr('src',data.doc_file);
    console.log(data);
});
