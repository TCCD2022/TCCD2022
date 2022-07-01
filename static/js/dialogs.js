$( function() {
    var dialog, form,
	// From http://www.whatwg.org/specs/web-apps/current-work/multipage/states-of-the-type-attribute.html#e-mail-state-%28type=email%29

      function saveChange() {
      }
      

    dialog = $( "#dialog-form" ).dialog({
      autoOpen: false,
      height: 400,
      width: 350,
      modal: true,
      buttons: {
        "Save change": saveChange,
        Cancel: function() {
          dialog.dialog( "close" );
        }
      },
      close: function() {
        form[ 0 ].reset();
        allFields.removeClass( "ui-state-error" );
      }
    });
 
    form = dialog.find( "form" ).on( "submit", function( event ) {
      event.preventDefault();
      // addUser();
    });
 
    $( document ).button().on( "click",".edit-col-type", function() {
	dialog.dialog( "open" );
	console.log("Clicked edit type button");
	var label = $("#chtype");
	var tcol = $(this).siblings().first();
	label.text(tcol.text());
	label.attr("col-id",tcol.attr("col-id"));
    });
});
