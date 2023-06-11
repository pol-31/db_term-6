$("button[name='btn_delete_marks']").click(function() {
    var marks_info = $(this).data('marks_info');
    var marks_data = marks_info.split('|');
    var fk_student_id = marks_data[0];
    var fk_subject = marks_data[1];
    
    var data = {
        fk_student_id: fk_student_id,
        fk_subject: fk_subject
    };

    $.ajax({
        type: 'POST',
        url: "/delete_marks",
        data: data,
        dataType: "text",
        success: function(resultData) {
            location.reload();
        }
    });
});


$("button[name='btn_edit_marks']").click(function() {
    window.location = "edit_marks?fk_student_id=" + $(this).data('stud_id') + "&fk_subject=" + $(this).data('subj_id');
});


$("button[name='btn_new_marks']").click(function() {

    window.location = "new_marks";

});






