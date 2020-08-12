 $(document).ready(function() {
    $('#id_Cool_Story_0').change(function() {
          var checkBox = document.getElementById('id_Cool_Story_0');
          if (checkBox.checked == true){
                console.log("ПОШЛА");
                document.getElementById('ASU_VP').style.display = 'block';
                    var Desc = document.getElementById('Description');
                    if(Desc.value == ""){
                        document.getElementById('Description').value += "Прошу предоставить доступ к системе АСУ ВП.\n";
                        }
                    else{
                        document.getElementById('Description').value += "\nПрошу предоставить доступ к системе АСУ ВП.\n";
                        }
            } else {
                console.log("УШЛА");
                document.getElementById('ASU_VP').style.display = 'none';
                var Desc = document.getElementById('Description');
                    if(Desc.value == ""){
                        }
                    else{
                        Desc.value = Desc.value.replace('\nПрошу предоставить доступ к системе АСУ ВП.\n','');
                        Desc.value = Desc.value.replace('Прошу предоставить доступ к системе АСУ ВП.\n','');
                        }
                    }
    });
    $('#id_Cool_Story_1').change(function() {
          var checkBox = document.getElementById('id_Cool_Story_1');
          if (checkBox.checked == true){
                document.getElementById('1C_ADD').style.display = 'block';
                var Desc = document.getElementById('Description');
                if(Desc.value == ""){
                        document.getElementById('Description').value += "Прошу предоставить доступ к системе 1C Русагротранс.\nИнформационные базы: ";
                        }
                    else{
                        document.getElementById('Description').value += "\nПрошу предоставить доступ к системе 1C Русагротранс.\nИнформационные базы: ";
                        }
            } else {
                console.log("УШЛА");
                document.getElementById('1C_ADD').style.display = 'none';
                    var Desc = document.getElementById('Description');
                    if(Desc.value == ""){
                        }
                    else{
                        Desc.value = Desc.value.replace('\nПрошу предоставить доступ к системе 1C Русагротранс.\nИнформационные базы: ','');
                        Desc.value = Desc.value.replace('Прошу предоставить доступ к системе 1C Русагротранс.\nИнформационные базы: ','');
                        }
                    }
    });
    $('#id_Cool_Story_2').change(function() {
          var checkBox = document.getElementById('id_Cool_Story_2');
          if (checkBox.checked == true){
                document.getElementById('ASU_MR').style.display = 'block';
                var Desc = document.getElementById('Description');
                if(Desc.value == ""){
                        document.getElementById('Description').value += "Прошу предоставить доступ к системе АСУ МР Русагротранс\n";
                        }
                    else{
                        document.getElementById('Description').value += "\nПрошу предоставить доступ к системе АСУ МР Русагротранс\n";
                        }
            } else {
                // Реализация процесса очистки доп опций.
                document.getElementById('ASU_MR').style.display = 'none';
                var Desc = document.getElementById('Description');
                    if(Desc.value == ""){
                        }
                    else{
                        Desc.value = Desc.value.replace('\nПрошу предоставить доступ к системе АСУ МР Русагротранс\n','');
                        Desc.value = Desc.value.replace('Прошу предоставить доступ к системе АСУ МР Русагротранс\n','');
                        }
                    }
    });
   $('#id_Cool_Story_3').change(function() {
          var checkBox = document.getElementById('id_Cool_Story_3');
          if (checkBox.checked == true){
                 console.log("ПОШЛА");
                document.getElementById('File_ADD').style.display = 'block';
                var Desc = document.getElementById('Description');
                if(Desc.value == ""){
                        document.getElementById('Description').value += "Прошу предоставить доступ к файловому хранилищу Русагротранс.\nПапка: ";
                        }
                    else{
                        document.getElementById('Description').value += "\nПрошу предоставить доступ к файловому хранилищу Русагротранс.\nПапка: ";
                        }
            } else {
                console.log("УШЛА");
                document.getElementById('File_ADD').style.display = 'none';
                    var Desc = document.getElementById('Description');
                    if(Desc.value == ""){
                        }
                    else{
                        Desc.value = Desc.value.replace('\nПрошу предоставить доступ к файловому хранилищу Русагротранс.\nПапка: ','');
                        Desc.value = Desc.value.replace('Прошу предоставить доступ к файловому хранилищу Русагротранс.\nПапка: ','');
                        }
                    }
    });
    $('#id_Cool_Story_4').change(function() {
          var checkBox = document.getElementById('id_Cool_Story_4');
          if (checkBox.checked == true){
                 console.log("ПОШЛА");
                document.getElementById('Remote_ADD').style.display = 'block';
                var Desc = document.getElementById('Description');
                if(Desc.value == ""){
                        document.getElementById('Description').value += "Прошу предоставить Удаленный доступ к Терминальному серверу MSKTSRAT.\n";
                        temp_terminal = "к Терминальному серверу MSKTSRAT.\n"
                        }
                    else{
                        document.getElementById('Description').value += "\nПрошу предоставить Удаленный доступ к Терминальному серверу MSKTSRAT.\n";
                        temp_terminal = "к Терминальному серверу MSKTSRAT.\n"
                        }
            } else {
                console.log("УШЛА");
                document.getElementById('Remote_ADD').style.display = 'none';
                var Desc = document.getElementById('Description');
                if(Desc.value == ""){
                        }
                    else{
                        Desc.value = Desc.value.replace('\nПрошу предоставить Удаленный доступ к Терминальному серверу MSKTSRAT.\n','');
                        Desc.value = Desc.value.replace('Прошу предоставить Удаленный доступ к Терминальному серверу MSKTSRAT.\n','');
                        Desc.value = Desc.value.replace('\nПрошу предоставить Удаленный доступ ','');
                        Desc.value = Desc.value.replace('Прошу предоставить Удаленный доступ ','');
                        }
                    }
    });
    $('#id_Cool_Story_5').change(function() {
          var checkBox = document.getElementById('id_Cool_Story_5');
          if (checkBox.checked == true){
                document.getElementById('RAT_Online_ADD').style.display = 'block';
                var Desc = document.getElementById('Description');
                if(Desc.value == ""){
                        document.getElementById('Description').value += "Прошу предоставить доступ к системе Русагротранс Онлайн \n";
                        }
                    else{
                        document.getElementById('Description').value += "\nПрошу предоставить доступ к системе Русагротранс Онлайн \n";
                        }
            } else {
                document.getElementById('RAT_Online_ADD').style.display = 'none';
                var Desc = document.getElementById('Description');
                if(Desc.value == ""){
                        }
                    else{
                        Desc.value = Desc.value.replace('\nПрошу предоставить доступ к системе Русагротранс Онлайн \n','');
                        Desc.value = Desc.value.replace('Прошу предоставить доступ к системе Русагротранс Онлайн \n','');
                        }
                    }
    });
    $('#id_Cool_Story_6').change(function() {
          var checkBox = document.getElementById('id_Cool_Story_6');
          if (checkBox.checked == true){
                var Desc = document.getElementById('Description');
                if(Desc.value == ""){
                        document.getElementById('Description').value += "Прошу предоставить доступ к Порталу Русагротранс \n";
                        }
                    else{
                        document.getElementById('Description').value += "\nПрошу предоставить доступ к Порталу Русагротранс \n";

                        }
            } else {
                document.getElementById('RAT_Online_ADD').style.display = 'none';
                var Desc = document.getElementById('Description');
                if(Desc.value == ""){
                        }
                    else{
                        Desc.value = Desc.value.replace('\nПрошу предоставить доступ к Порталу Русагротранс \n','');
                        Desc.value = Desc.value.replace('Прошу предоставить доступ к Порталу Русагротранс \n','');
                        }
                    }
    });
    $('#RDP_PC').change(function() {
          var checkBox = document.getElementById('RDP_PC');
          if (checkBox.checked == true){
                console.log("РАБОЧИЙ ПК")
                document.getElementById('computername').style.display = 'table-cell';
                var Desc = document.getElementById('Description');
                if(Desc.value == ""){
                        document.getElementById('Description').value += "к Рабочему ПК: "+document.getElementById('compname').value+"\n";
                        temp_pc = "к Рабочему ПК: "+document.getElementById('compname').value+"\n"
                        console.log(temp_pc)
                        }
                    else{
                        document.getElementById('Description').value += "к Рабочему ПК: "+document.getElementById('compname').value+"\n";
                        temp_pc = "к Рабочему ПК: "+document.getElementById('compname').value+"\n"
                        console.log(temp_pc)
                        }
            } else {
                document.getElementById('computername').style.display = 'none';
                var Desc = document.getElementById('Description');
                if(Desc.value == ""){
                        }
                    else{
                        console.log(temp_pc)
                        Desc.value = Desc.value.replace(temp_pc,'');

                        }
                    }
    });
   //outer_user
    $('#outer_user').change(function() {
          var checkBox = document.getElementById('outer_user');
          if (checkBox.checked == true){
                document.getElementById('outer_user_selector').style.display = 'block';
                document.getElementById('new_user').disabled = true;
            } else {
                document.getElementById('outer_user_selector').style.display = 'none';
                document.getElementById('new_user').disabled = false;
                }
    });
    //new_user
        $('#new_user').change(function() {
          var checkBox = document.getElementById('new_user');
          if (checkBox.checked == true){
                //document.getElementById('outer_user_selector').style.display = 'block';
                document.getElementById('outer_user').disabled = true;
            } else {
                //document.getElementById('outer_user_selector').style.display = 'none';
                document.getElementById('outer_user').disabled = false;
                }
    });
   // Option selector RDP
    $('#RDP_TERMINAL').change(function() {
          var checkBox = document.getElementById('RDP_TERMINAL');
          if (checkBox.checked == true){
                console.log("РАБОЧИЙ ПК")
                var Desc = document.getElementById('Description');
                if(Desc.value == ""){
                        document.getElementById('Description').value += "к Терминальному серверу MSKTSRAT.\n";
                        temp_terminal = "к Терминальному серверу MSKTSRAT.\n"
                        }
                    else{
                        document.getElementById('Description').value += "к Терминальному серверу MSKTSRAT.\n";
                        temp_terminal = "к Терминальному серверу MSKTSRAT.\n"
                        }
            } else {
                document.getElementById('computername').style.display = 'none';
                var Desc = document.getElementById('Description');
                if(Desc.value == ""){
                        }
                    else{

                        Desc.value = Desc.value.replace(temp_terminal,'');

                        }
                    }
    });
});