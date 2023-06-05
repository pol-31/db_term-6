$("button[name='btn_delete_pt']").click(function() {

    var data = { pt_id : $(this).data('id')}

    $.ajax({
      type: 'POST',
      url: "/delete_pt",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_pt']").click(function() {

    window.location = "edit_pt?pt_id="+$(this).data('id');

});


$("button[name='btn_new_pt']").click(function() {

    window.location = "new_pt";

});


