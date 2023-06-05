$("button[name='btn_delete_eo']").click(function() {

    var data = { eo_id : $(this).data('id')}

    $.ajax({
      type: 'POST',
      url: "/delete_eo",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_eo']").click(function() {

    window.location = "edit_eo?eo_id="+$(this).data('id');

});


$("button[name='btn_new_eo']").click(function() {

    window.location = "new_eo";

});

