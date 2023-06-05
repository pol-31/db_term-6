$("button[name='btn_db_switch']").click(function() {
  $.ajax({
    type: 'GET',
    url: "/switch_db",
    success: function(resultData) {
      location.reload();
    }
  });
});

