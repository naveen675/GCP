function transformCSVtoJSON(line) {
  var values = line.split(',');
  var properties = [
    'eno',
    'empname'
  ];
  var weatherInCity = {};

  for (var count = 0; count < values.length; count++) {
    if (values[count] !== 'null') {
      weatherInCity[properties[count]] = values[count];
    }
  }

  var jsonString = JSON.stringify(weatherInCity);
  return jsonString;
}


function transform(line) {
var valuelist = line.split(',');
var obj = new Object();
obj.eno = valuelist[0];
obj.empname = valuelist[1];
var jsonString = JSON.stringify(obj);

return jsonString;
}