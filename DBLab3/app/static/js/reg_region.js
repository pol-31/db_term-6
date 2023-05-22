$("button[name='btn_delete_reg_region']").click(function() {

    var data = { reg_region_id : $(this).data('id')}

    $.ajax({
      type: 'POST',
      url: "/delete_reg_region",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_reg_region']").click(function() {

    window.location = "edit_reg_region?reg_region_id="+$(this).data('id');

});


$("button[name='btn_new_reg_region']").click(function() {

    window.location = "new_reg_region";

});


