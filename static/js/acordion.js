
jQuery(document).ready(function(){
    $('.caret').click(function(e) {
	e.preventDefault();
	$('.selected').removeClass('selected');
	$(this).addClass('selected');
    });
});
   
var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
    toggler[i].addEventListener("click", function(e) {
	$('#file_col_name').html($(this).text());
	var url3 = $(this).attr('find-file-results-url');
	console.log(url3)
	standardize = true
	$.ajax({
	    url:url3,
	    type:"GET",
	    // data:{sd:standardize},
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
		    
    		    console.log(result.results[0]);
    		} else {
    		    $iframe.attr('src','');
    		}
		
		console.log(result)
	    },
	    error:function(error){
		// alert(error)
		console.log(`Error "${error}"`) || alert(error)
	    }
	})
	this.parentElement.querySelector(".nested").classList.toggle("active");
	this.classList.toggle("caret-down");
  });
} 

$( ".results_list" ).on('select2:select', function (e) {
    var data = e.params.data;
    var $iframe = $('#panel-res');
     $iframe.attr('src',data.file_path.slice(5));
    console.log(data);
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$(function() {
    // https://swisnl.github.io/jQuery-contextMenu/docs.html";
    var itemsDisabled = {};
    $.contextMenu({
        selector: '.context-menu-one', 
	callback: function(key, options) {
	    // var tmp = "/home/rstudio/data/" + $(this).text().trim();

	    var m = "clicked: " + key;
	    switch (key) {
	    case "metadata":
		var url3 = $(this).attr('doc-url');
		var elementId = '#'+$(this).attr('id');
		var parent = $(this).parent().children('ul')
		// $(this).parent().css( "background-color", "red" );
		$.ajax({
		    // url: Url,
		    url:url3,
		    dataType: "json",
		    type:"GET",
		    // data: data_file,
		    success: function(result){
			if (result.supported == true) {
			    $('[data-toggle="tooltip"]').tooltip();
			    $(elementId).tooltip('dispose').attr('title',
								 "Rows: " + result.numrows[0] +
								 " Columns: " + result.numcols[0] +
								 " Size: " + result.filesize[0]);
			    
			    Object.entries(result.colurl).forEach(([k,v]) => {
				var titulo = v['type']+ ',&nbsp;' + v['scale'];
				parent.append('<li> <div class="parent">' +
						' <input type="checkbox" id= ' + v['id'] + ' value = '+k+'>'+
						 '<label  class = "nav-link context-menu-cols fcol" col-id = ' + v['id'] +
						 ' for = ' + v['id'] + ' title = ' + titulo +
						 ' vis-col-url= '+ v['vis-col-url'] + '> &nbsp;' +
						 k + '</label> <button class="ihide fa fa-edit  edit-col-type"></button>' +
						 '</div>' +
						 '</li>');
			    })
			    console.log(result)
			    alert("Metadata extracted\nHover on the filename");
			}
			// console.log("parent:" + parent.html())
			// console.log(result) || alert(result.result + "\nHover on the filename");
		    },
		    error:function(error){
			// alert(error)
			console.log(`Error "${error}"`) || alert(error)
		    }
		})
		// window.console && console.log(url3) || alert(url3);
		break;

	    case "clean":
		var url3 = $(this).attr('clean-metadoc-url');
		$.ajax({
		    url:url3,
		    dataType: "json",
		    type:"POST",
		    data: { csrfmiddlewaretoken: getCookie('csrftoken') },
		    success: function(result){
			var dfile = $(".selected");
			dfile.siblings().children().empty();
			$('[data-toggle="tooltip"]').tooltip();
			dfile.tooltip('dispose').attr('title','Metadata not extracted');
			console.log(dfile.text()) || alert(result);
		    },
		    error:function(error){
			// alert(error)
			console.log(`Error "${error}"`) || alert(error)
		    }
		})
		window.console && console.log(m) || alert(url3);
		break;
	    // case "visualization":
	    // 	alert(key);
	    // 	break;
	    // case "process":
	    // 	alert(key);
	    // 	break;
	    }
	},
	items: {
	    "metadata": {name: "Extract metadata", icon:  "fas fa-tags" },

	    "sep1": "---------",
	    // https://stackoverflow.com/questions/7751824/jquery-context-menu-disable-menu-items
	    "clean": {name: "Clean metadata", icon: "delete",
		      disabled: function(key, opt) {
		      	   return !!itemsDisabled[key];
		      }
		     },
	}
    });
    itemsDisabled["clean"] = true;


    $('.context-menu-one').on('click', function(e){
	console.log('clicked', this);
    })

});



$( document ).on('click','.context-menu-cols', function(e){
    	// console.log('clicked', this);
    	var url3 = $(this).attr('vis-col-url');
    	$.ajax({
    	    url:url3,
    	    dataType: "json",
    	    type:"GET",
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
		    
    		    console.log(result.results[0]);
    		} else {
    		    $iframe.attr('src','');
    		}
    		// $.each(result.items, function (i, item){
    		console.log(result.results.length);
    		//    console.log(item);
    		// });
    		// console.log(result) || alert(result)
    		return {
    		    results: result.items
    		}
    	    },
    	    error:function(error){
    		console.log(`Error "${error}"`) || alert(error)
    	    }
    	});
    	// window.console && console.log(url3) || alert(url3);

    })
