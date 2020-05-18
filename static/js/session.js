

// ajax
$(document).ready(
    function () {
        showSession();
        session();

    }
);


// save data
var button;
function session() {
    button = document.getElementById('click');
    button.onclick = function () {
        saveSession();
        // var table = document.getElementById('show-data');
        // table.innerHTML = "";
        // showSession();
        var table = document.getElementById('show-data');
        $('#show-data').empty();

        setTimeout(function () { showSession(); }, 0);
    };
}



function saveSession() {

    var getSession = document.getElementById('session').value;

    if (getSession != "") {

        var saveUrl = 'save?name=' + getSession;


        var req = new XMLHttpRequest();
        req.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                result = req.responseText;

                // check if it is true or not
                if (result == 'true') {

                    Swal.fire({
                        icon: 'success',
                        title: 'Congratulations',
                        text: 'Successfully added',

                    });

                    document.getElementById('session').value = "";


                }
                else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Something went wrong!',

                    });

                }
                // setTimeout(function () { showSession(); }, 3000);

            }
        };
        req.open("GET", saveUrl, true);
        req.send();
    }
}

// show list
function showSession() {
    url = "{% url 'show_session' %}"
    var rqst = new XMLHttpRequest();
    rqst.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var data = eval(this.responseText);
            var table = document.getElementById('show-data');

            for (var i = 0; i < data.length; i++) {
                var row = `<tr>
            <td>${i + 1}</td>
            <td>${data[i].session_name}</td>
            <td style="width: 40px">
              <button class="btn btn-primary btn-xs"><i class="fas fa-pen" style="color: white;"></i></button>
            </td>
            <td style="width: 40px">
              <button class="btn btn-danger btn-xs"><i class="fas fa-trash" style="color: white;"></i></button>
            </td>
          </tr>`
                table.innerHTML += row
            }
            data = data.value = "";

        }
    };
    rqst.open("GET", url, true);
    rqst.send();
}


