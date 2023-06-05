$("button[name='btn_delete_region']").click(function() {

    var data = { region_id : $(this).data('id')}

    $.ajax({
      type: 'POST',
      url: "/delete_region",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_region']").click(function() {

    window.location = "edit_region?region_id="+$(this).data('id');

});


$("button[name='btn_new_region']").click(function() {

    window.location = "new_region";

});


