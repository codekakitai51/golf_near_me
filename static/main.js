function generateDates() {
  var dateSelect = document.getElementById('dateSelect');
  var currentDate = new Date();
  var hours = currentDate.getHours();
  if (hours >= 21) {
    currentDate.setDate(currentDate.getDate() + 1);
  }

  var twoWeekLaterDate = new Date();
  twoWeekLaterDate.setDate(currentDate.getDate() + 14); 

  while (currentDate <= twoWeekLaterDate) {
      var option = document.createElement('option');
      const dd = String(currentDate.getDate()).padStart(2, '0');  
      const mm = String(currentDate.getMonth() + 1).padStart(2, '0');  
      const yyyy = currentDate.getFullYear();  
      const formattedDate = mm + '/' + dd + '/' + yyyy;
      option.value = formattedDate;

      option.text = currentDate.toDateString();
      dateSelect.add(option);
      currentDate.setDate(currentDate.getDate() + 1);
  }
}


function generateTimes() {
  var timeSelect = document.getElementById('timeSelect');
  var time = 8

  while (time <= 16) {
    var option = document.createElement('option');
    if (time == 12) {
      option.value = "_" + time + "PM"
      option.text = time + ':00 PM'
    } else if (time >= 13) {
      option.value = "_" + (time - 12) + 'PM'
      option.text = time - 12 + ':00 PM'
    } else {
      if (time <= 9) {

        option.value = '_' + time + 'AM'
        option.text = time + ':00 AM'
      }
      option.value = '_' + time + 'AM'
      option.text = time + ':00  AM'
    }
    timeSelect.add(option)
    time += 1
  }
}

window.onload = function() {
  generateDates();
  generateTimes();
};