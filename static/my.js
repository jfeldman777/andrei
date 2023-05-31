// js.html
  window.onload = function () {
    var tables = document.getElementsByTagName("table");
    for (var i = 0; i < tables.length; i++) {

      var rows = tables[i].getElementsByTagName("tr");
      for (var j = 0; j < rows.length; j++) {
        var cells = rows[j].getElementsByTagName("td");
        for (var k = 0; k < cells.length; k++) {


          if (tables[i].classList.contains("dif")) {
            if (cells[k].innerHTML < 0) {
              cells[k].style.backgroundColor = "pink";
            } else if (cells[k].innerHTML == 0) {
              cells[k].style.backgroundColor = "yellow";
            } else
              cells[k].style.backgroundColor = "white";
          }


          if (tables[i].classList.contains("balance")) {
            if (cells[k].innerHTML < 0) {
              cells[k].style.backgroundColor = "pink";
            } else
              if (cells[k].innerHTML > 0) {
                cells[k].style.backgroundColor = "lightblue";
              }
          }


        }
      }
    }
  };
///////////////////////////////// menu2.html 
  var f1 = 'f10'
  var element;
  var a = "/s1/";

  $('td.good').click(function () {

    var p = $(this).attr("key");
    a = $(this).attr("action");
    f1 = $(this).attr("fname");


    var originalValue = $(this).text();

    var x = $.trim(originalValue);
    if (x == '0') x = '';

    var ID = new Date().getTime();
    $(this).html('<input type="text" id=' + ID + ' size="1" maxlength="4" value="' + x + '">');

    element = document.getElementById(ID);
    element.focus();



    $(this).on('keypress', '#' + ID, function (event) {

      if (event.which === 13) { // 13 соответствует клавише Enter
        element.blur();

      }
    });




    $('td input').focusout(function () {

      var newValue = $(this).val();

      var iV = parseInt(newValue)
      if (iV == NaN || iV < 0) return;

      $(this).parent().text(newValue + '@');

      var form = document.getElementById(f1);
      form.action = a


      button = form.querySelector(".button3");
      button.disabled = false;

      // Create a new hidden input element
      var input = document.createElement('input');

      input.type = 'hidden';
      input.name = p;
      input.value = newValue;
      var cellWidth = $(this).clientWidth - 4;
      var cellHeight = $(this).clientHeight - 2;

      var container = $(this)
      input.style.width = cellWidth + "px";
      input.style.height = cellHeight + "px";
      //Add the new input element to the form
      form.appendChild(input);


    });
  });