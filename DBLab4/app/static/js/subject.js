$("button[name='btn_delete_subject']").click(function() {

    var data = { subject_id : $(this).data('id')}

    $.ajax({
      type: 'POST',
      url: "/delete_subject",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_subject']").click(function() {

    window.location = "edit_subject?subject_id="+$(this).data('id');

});


$("button[name='btn_new_subject']").click(function() {

    window.location = "new_subject";

});

