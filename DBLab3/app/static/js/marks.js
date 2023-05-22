$("button[name='btn_delete_marks']").click(function() {
    var marks_info = $(this).data('marks_info');
    var marks_data = marks_info.split('|');
    var marks_fk_student_id = marks_data[0];
    var marks_fk_subject = marks_data[1];
    
    var data = {
        marks_fk_student_id: marks_fk_student_id,
        marks_fk_subject: marks_fk_subject
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
    var marks_info = $(this).data('marks_info');
    var marks_data = marks_info.split('|');
    var marks_fk_student_id = marks_data[0];
    var marks_fk_subject = marks_data[1];
    window.location = "edit_marks?marks_fk_student_id=" + marks_fk_student_id + "&marks_fk_subject=" + marks_fk_subject;
});


$("button[name='btn_new_marks']").click(function() {

    window.location = "new_marks";

});






