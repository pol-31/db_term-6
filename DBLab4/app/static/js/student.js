$("button[name='btn_delete_student']").click(function() {

    var data = { student_id : $(this).data('id')}

    $.ajax({
      type: 'POST',
      url: "/delete_student",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_student']").click(function() {

    window.location = "edit_student?student_id="+$(this).data('id');

});


$("button[name='btn_new_student']").click(function() {

    window.location = "new_student";

});


