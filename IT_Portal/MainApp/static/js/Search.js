function SearchTable(name,table_name) {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById(name);
  filter = input.value.toUpperCase();
  table = document.getElementById(table_name);
  tr = table.getElementsByTagName("tr");
  console.log('ПОгнали ' + input.value)
  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i];
    //console.log(td)
    if (td) {
      txtValue = td.textContent || td.innerText;
      //console.log('TD = ' + txtValue)
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        console.log(tr[i])
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}