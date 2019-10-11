<?php


include_once(dirname(__FILE__).'/../configwizardhelper.inc.php');




wizardbnd_configwizard_init();

function wizardbnd_configwizard_init(){
	

	$name="wizardbnd";
	

	$args=array(
		CONFIGWIZARD_NAME => $name,
		CONFIGWIZARD_TYPE => CONFIGWIZARD_TYPE_MONITORING,
		CONFIGWIZARD_DESCRIPTION => "This Nagios XI wizard allows you to bulk monitoring network switch and router port status and bandwidth.", 
		CONFIGWIZARD_DISPLAYTITLE => "Bulk Network Devices",
		CONFIGWIZARD_FUNCTION => "wizardbnd_configwizard_func",
		CONFIGWIZARD_PREVIEWIMAGE => "wizardbnd.jpg",
		CONFIGWIZARD_VERSION => "0.1",
		CONFIGWIZARD_DATE => "2019-09-30",
		CONFIGWIZARD_COPYRIGHT => "",
		CONFIGWIZARD_AUTHOR => "Demetrius Papadimitriou",
		);

	register_configwizard($name,$args);
	}


function wizardbnd_configwizard_func($mode="",$inargs=null,&$outargs,&$result){
	
	$wizard_name="wizardbnd";


	$result=0;
	$output="";
	

	$outargs[CONFIGWIZARD_PASSBACK_DATA]=$inargs;


	switch($mode){
		case CONFIGWIZARD_MODE_GETSTAGE1HTML:
			
			
			$back = htmlentities(grab_array_var($_POST,'backButton',false),ENT_QUOTES); 
			

			if(!$back) 
			{
			
				unset($_SESSION['wizardbnd']); 
				$_SESSION['wizardbnd'] = array(); 
				$hostname = ''; 

			}	
			else 
			{			

				$hostname = $_SESSION['wizardbnd']['hostname'];  
			}
			shell_exec("python3.6 /usr/local/nagiosxi/html/includes/configwizards/wizardbnd/moveFiles.py");
			@unlink('/usr/local/nagiosxi/html/config/uploads/FILE.xlsx');
	
			$output='
			
			
			<h4><b><p>Please submit your IP list below :</p></b></h4><p>(example:192.168.1.2,192.168.1.3)</p><br />			
			<textarea name="hostname" rows="5" cols="100"></textarea><br/> <br/>	<br/>	
			<h4><p style="font-weight:bold;">OR UPLOAD AN .XLSX FILE :</p></h4>			
			<input type="file" name="afile" id="afile" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"/>
			<p>System prioritizes file input. In the case of a file input ,text input (IP list) will be ignored!</p>
			<p id="message"></p>
			<br/>	
			<script>
			document.querySelector(\'#afile\').addEventListener(\'change\', function(e) {
			  var file = this.files[0];
			  var fd = new FormData();
			  fd.append("afile", file);
			 
			  var xhr = new XMLHttpRequest();
			  xhr.open(\'POST\', \'handle_file_upload.php\', true);
			  
			  xhr.upload.onprogress = function(e) {
				if (e.lengthComputable) {
				  var percentComplete = (e.loaded / e.total) * 100;
				  console.log(percentComplete + \'% uploaded\');
				}
			  };

			  xhr.send(fd);
			}, false);
			</script>
			
			<h4>Select the Warning and Critical rate below: </h4>
			<table class="table table-condensed table-no-border table-auto-width">
				<tbody><tr>
					<td>
						<label for="warn_speed_in_percent">Warning: Input Rate:</label>
					</td>
					<td>
						<input class="form-control" type="text" value="50" name="warn_speed_in_percent" size="2"> %
					</td>
					<td>
						<label for="crit_speed_in_percent">Critical: Input Rate:</label>
					</td>
					<td>
						<input class="form-control" type="text" value="80" name="crit_speed_in_percent" size="2"> %
					</td>
				</tr>
				<tr>
					<td>
						<label for="warn_speed_in_percent">Warning: Output Rate:</label>
					</td>
					<td>
						<input class="form-control" type="text" value="50" name="warn_speed_out_percent" size="2"> %
					</td>
					<td>
						<label for="crit_speed_in_percent">Critical: Output Rate:</label>
					</td>
					<td>
						<input class="form-control" type="text" value="80" name="crit_speed_out_percent" size="2"> %
					</td>
				</tr>
			</tbody>			
			</table>
			<br>
			<h5><b>Create contact and host groups : <input type="checkbox" name="group" value="value1" checked></b></h5> 
			<br>
			<p>Click <b>Next</b> to continue.</p>
			';
			
			break;

		case CONFIGWIZARD_MODE_VALIDATESTAGE1DATA:
		
			$errors=0;
			$errmsg=array();			
			
			$hostname=$_SESSION['wizardbnd']['hostname']=grab_array_var($inargs,"hostname");
			$hostnamecomma = str_replace("\n",",",$hostname); 
			$ip_arr = str_replace(" ",",",$hostnamecomma); 
			$_SESSION['wizardbnd']['ipresult']=$ipresult=shell_exec("python3.6 /usr/local/nagiosxi/html/includes/configwizards/wizardbnd/checkHosts.py $ip_arr");
			$tfarray=explode("],", $ipresult);
			$hosts=$tfarray[0];			
			$hosts2=$tfarray[2];
			preg_match_all('/(\d+)\.(\d+)\.(\d+)\.(\d+)/', $hosts, $output_array);				
			preg_match_all('/(\d+)\.(\d+)\.(\d+)\.(\d+)/', $hosts2, $output_array2);
			
			if (!(preg_match_all('/(\d+)\.(\d+)\.(\d+)\.(\d+)/', $hosts, $output_array) || preg_match_all('/(\d+)\.(\d+)\.(\d+)\.(\d+)/', $hosts2, $output_array2))) {
				$errmsg[$errors++]="Please give useful input!";	
			}		
			if($errors>0){
				$outargs[CONFIGWIZARD_ERROR_MESSAGES]=$errmsg;
				$result=1;
				}				
				
			break;
		case CONFIGWIZARD_MODE_GETSTAGE2HTML:
					
			
			//$back = htmlentities(grab_array_var($_POST,'backButton',false),ENT_QUOTES); 
			
			$test = grab_array_var($inargs,"warn_speed_in_percent");
			if (empty($test)) {
				$hostname=$_SESSION['wizardbnd']['hostname'];
				$checked=false;
				$warn_speed_in_percent=$_SESSION['wizardbnd']['warn_speed_in_percent'];
				$crit_speed_in_percent=$_SESSION['wizardbnd']['crit_speed_in_percent'];
				$warn_speed_out_percent=$_SESSION['wizardbnd']['warn_speed_out_percent'];
				$crit_speed_out_percent=$_SESSION['wizardbnd']['crit_speed_out_percent'];
			}else{
				$hostname=$_SESSION['wizardbnd']['hostname'];
				$checked=grab_array_var($inargs,"group");
				$warn_speed_in_percent=$_SESSION['wizardbnd']['warn_speed_in_percent']=grab_array_var($inargs,"warn_speed_in_percent");
				$crit_speed_in_percent=$_SESSION['wizardbnd']['crit_speed_in_percent']=grab_array_var($inargs,"crit_speed_in_percent");
				$warn_speed_out_percent=$_SESSION['wizardbnd']['warn_speed_out_percent']=grab_array_var($inargs,"warn_speed_out_percent");
				$crit_speed_out_percent=$_SESSION['wizardbnd']['crit_speed_out_percent']=grab_array_var($inargs,"crit_speed_out_percent");	
			}	
			

			$checked=grab_array_var($inargs,"group");	
			
			if ($checked == 'value1'){
				shell_exec("python3.6 /usr/local/nagiosxi/html/includes/configwizards/wizardbnd/group_creator.py");										
			}			
						
			$ipresult=$_SESSION['wizardbnd']['ipresult'];
			$tfarray=explode("],", $ipresult);
			
			$hosts=$tfarray[0];			
			$hosts1=$tfarray[1];
			$hosts2=$tfarray[2];
			$hosts3=$tfarray[3];
			preg_match_all('/(\d+)\.(\d+)\.(\d+)\.(\d+)/', $hosts, $output_array);	
			preg_match_all('/(\d+)\.(\d+)\.(\d+)\.(\d+)/', $hosts1, $output_array1);
			preg_match_all('/(\d+)\.(\d+)\.(\d+)\.(\d+)/', $hosts2, $output_array2);
			preg_match_all('/(\d+)\.(\d+)\.(\d+)\.(\d+)/', $hosts3, $output_array3);
			$okips = array_merge($output_array[0], $output_array2[0]);
			
			$str = implode(",",$okips);
			
			$complete=array();
			$grouplists = shell_exec("python3.6 /usr/local/nagiosxi/html/includes/configwizards/wizardbnd/group_fetch.py");

			$tfarray2=explode("],", $grouplists);

			$clean=array();
			$cleaner=array();
			foreach ($tfarray2 as &$value) {
				$clean=array();
				$group=explode(",", $value);
				
				foreach($group as &$value1){
					preg_match("/'(.*)'/", $value1, $output_array71);					
					array_push($clean,$output_array71[1]);
				}
				array_push($cleaner,$clean);
			}

			if(file_exists('/usr/local/nagiosxi/html/config/uploads/FILE.xlsx')){
			$table= shell_exec("python3.6 /usr/local/nagiosxi/html/includes/configwizards/wizardbnd/table.py $str");
			$tfarray1=explode("],", $table);
			foreach ($tfarray1 as &$value) {
				preg_match("/'(.*)', '(.*)', '(.*)', '(.*)', (\d+.\d+), (\d+.\d+)/", $value, $output_array72);

				$values_array=array($output_array72[1],$output_array72[2],$output_array72[3],$output_array72[4],$output_array72[5],$output_array72[6]);
				array_push($complete,$values_array);
			}

			}else{
				
				foreach($okips as &$value){
					$values_array=array('Host :'.$value,$value,'hostgroup','contactgroup','37.9756512','23.7318121');
					array_push($complete,$values_array);
				}
				
			}			
			
			$table2= shell_exec("python3.6 /usr/local/nagiosxi/html/includes/configwizards/wizardbnd/bwtable.py $str $warn_speed_in_percent $crit_speed_in_percent $warn_speed_out_percent $crit_speed_out_percent");

			
			
			preg_match_all('/\'(\d+)\': \{\'Desc\': \'([^:{]+)\', \'Band\': \'(\d+.\d+)\', \'Alia\': \' \', \'scaledValues\': \[(\d+.\d+), (\d+.\d+), (\d+.\d+), (\d+.\d+)\], \'scale\': \'(Kbps|Mbps|bps)\', \'hostIP\': \'(\d+\.\d+\.\d+\.\d+)\'}/', $table2, $output_array91);
			
			$_SESSION['wizardbnd']['Descr'] = $output_array91[2];			
			
			$output='
			<script type="text/javascript">
			function fnExcelReport(tableID)
			{
				var tab_text="<table border=\'2px\'><tr bgcolor=\'#87AFC6\'>";
				var textRange; var j=0;
				tab = document.getElementById(tableID); // id of table

				for(j = 0 ; j < tab.rows.length ; j++) 
				{     
					tab_text=tab_text+tab.rows[j].innerHTML+"</tr>";
					//tab_text=tab_text+"</tr>";
				}

				tab_text=tab_text+"</table>";
				tab_text= tab_text.replace(/<A[^>]*>|<\/A>/g, "");
				tab_text= tab_text.replace(/<img[^>]*>/gi,""); 
				tab_text= tab_text.replace(/<input[^>]*>|<\/input>/gi, ""); 

				var ua = window.navigator.userAgent;
				var msie = ua.indexOf("MSIE "); 

				if (msie > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./))      // If Internet Explorer
				{
					txtArea1.document.open("txt/html","replace");
					txtArea1.document.write(tab_text);
					txtArea1.document.close();
					txtArea1.focus(); 
					sa=txtArea1.document.execCommand("SaveAs",true,"Say Thanks to AlgoSys.xls");
				}  
				else                 //other browser not tested on IE 11
					sa = window.open(\'data:application/vnd.ms-excel,\' + encodeURIComponent(tab_text));  

				return (sa);
			}
			
				function hideShow() {
				  var x = document.getElementById("bwTable");
				  if (x.style.display === "block") {
					x.style.display = "none";
				  } else {
					x.style.display = "block";
				  }
				}	
			
			function change()
				{
					var elem = document.getElementById("btnReveal");
					if (elem.innerHTML=="SHOW MORE OPTIONS"){ 
						elem.innerHTML="SHOW LESS OPTIONS"; 
					}else {
						elem.innerHTML="SHOW MORE OPTIONS"
					}
				}					
			</script>
			
			<iframe id="txtArea1" style="display:none"></iframe>
			<h6>Status :</h6>
			<table id="headerTable" class="table table-condensed table-hover table-striped table-bordered table-auto-width" border="1"  height=100 width="600" class="standardtable">
					<tr>
							<th>Host</th>
							<th>Ping</th>
							<th>SNMP</th>
							
					</tr>
			'.hosts_status($output_array,$output_array1,$output_array2,$output_array3).'			
			</table>
			<button type ="button" id="btnExport" class="btn btn-sm btn-primary" onclick="fnExcelReport(\'headerTable\');"> DOWNLOAD TABLE </button><br/><br/>
			<h6>Options :</h6>
			<table id="headerTable1" class="table table-condensed table-hover table-striped table-bordered table-auto-width">
					<tr>
							<th>Host</th>
							<th>Ip</th>
							<th>Host Group</th>
							<th>Contact Group</th>
							<th>Latitude</th>
							<th>Longitude</th>	
							<th>CPU Warning Range</th>
							<th>CPU Critical Range</th>
							<th>Memory Warning Range</th>
							<th>Memory Critical Range</th>							
							<th>Temperature Warning Range</th>
							<th>Temperature Critical Range</th>						
							
					</tr>
			'.device_data($complete,$cleaner).'			
			</table>
			
			</table>
			<button type ="button" id="btnReveal" class="btn btn-sm btn-primary" onclick="hideShow();change();">SHOW MORE OPTIONS</button><br>
			<br><table id="bwTable" class="table table-condensed table-hover table-striped table-bordered table-auto-width" hidden>
					<tr>	
							<th>Host IP</th>
							<th>Port</th>
							<th>Port Description</th>
							<th>Max Speed</th>
							<th>Bandwidth</th>						
					</tr>
			'.bwtable($output_array91,$okips).'			
			</table>			
			
			<br/>
			<p><font color="red" size="3">Click <b>Next</b> to continue the process with the available hosts.</font></p>
			';


			
			break;
		
		
		case CONFIGWIZARD_MODE_VALIDATESTAGE2DATA:		
			
			
			$hostname_=$_SESSION['wizardbnd']['host_inputs']=grab_array_var($inargs,"host_inputs");
			$IP_=$_SESSION['wizardbnd']['IP']=grab_array_var($inargs,"IP");
			$_SESSION['wizardbnd']['host-selector']=grab_array_var($inargs,"host-selector");
			$_SESSION['wizardbnd']['contact-selector']=grab_array_var($inargs,"contact-selector");
			$lat_test=$_SESSION['wizardbnd']['lat_inputs']=grab_array_var($inargs,"lat_inputs");
			$long_test=$_SESSION['wizardbnd']['long_inputs']=grab_array_var($inargs,"long_inputs");

			$_SESSION['wizardbnd']['cpuwr']=grab_array_var($inargs,"cpuwr");
			$_SESSION['wizardbnd']['cpucr']=grab_array_var($inargs,"cpucr");
			$_SESSION['wizardbnd']['memwr']=grab_array_var($inargs,"memwr");
			$_SESSION['wizardbnd']['memcr']=grab_array_var($inargs,"memcr");
			$_SESSION['wizardbnd']['tempwr']=grab_array_var($inargs,"tempwr");
			$_SESSION['wizardbnd']['tempcr']=grab_array_var($inargs,"tempcr");
			
			$_SESSION['wizardbnd']['inbww']=grab_array_var($inargs,"inbww");
			$_SESSION['wizardbnd']['inbwc']=grab_array_var($inargs,"inbwc");
			$_SESSION['wizardbnd']['outbww']=grab_array_var($inargs,"outbww");
			$_SESSION['wizardbnd']['outbwc']=grab_array_var($inargs,"outbwc");
			$_SESSION['wizardbnd']['scaleSelector']=grab_array_var($inargs,"scaleSelector");
			
			$_SESSION['wizardbnd']['help']=grab_array_var($inargs,"help");
			$_SESSION['wizardbnd']['portNo']=grab_array_var($inargs,"portNo");
			
			$errors=0;
			$errmsg=array();
			
			foreach ($IP as &$value){
				if(!preg_match('/25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9]\.25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9]\.25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9]\.25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9]/', $value)){
					$errmsg[$errors++]="Wrong IP input detected!";					
				}
			}
			
			if(count(array_unique($hostname_))<count($hostname_)){
				$errmsg[$errors++]="You must input unique host names!";
			}
			
			if(count(array_unique($IP_))<count($IP_)){
				$errmsg[$errors++]="You must input unique IP addresses!";
			}
			
			foreach ($long_test as &$value){
				if(!preg_match('/\A-?[1-9][1-7]\d\z|\A-?[1-9]\d\z|\A-?180\z|\A-?[1-9][1-7]\d\.\d{1,7}\z|\A-?[1-9]\d\.\d{1,7}\z|\A-?180\.0{1,7}\z|\A-?0\.\d{1,7}\z|\A0\z/', $value)){
					$errmsg[$errors++]="Wrong Longitude input detected!format and range[-180.0000000,180.0000000]";					
				}
			}
			foreach ($lat_test as &$value){
				if(!preg_match('/\A-?[1-8]\d\z|\A-?[1-9]\z|\A-?90\z|\A-?[1-8]\d\.\d{1,7}\z|\A-?\d\.\d{1,7}\z|\A-?90\.0{1,7}\z|\A-?0\.\d{1,7}\z|\A0\z/', $value)){
					$errmsg[$errors++]="Wrong Latitude input detected! format and range[-90.0000000,90.0000000]";					
				}
			}
			
			
			
			if($errors>0){
				$outargs[CONFIGWIZARD_ERROR_MESSAGES]=$errmsg;
				$result=1;
				}
			
			break;
			

						
		case CONFIGWIZARD_MODE_GETSTAGE3HTML:
			

			$okip = $_SESSION['wizardbnd']['output_array'][0];
			$okip1 = $_SESSION['wizardbnd']['output_array2'][0];
			$checked=grab_array_var($inargs,"group");							
			$hostname=grab_array_var($inargs,"hostname");			

			$host_inputs=$_SESSION['wizardbnd']['host_inputs'];
			$IP=$_SESSION['wizardbnd']['IP'];
			$host_selector=$_SESSION['wizardbnd']['host-selector'];
			$contact_selector=$_SESSION['wizardbnd']['contact-selector'];
			$lat_inputs=$_SESSION['wizardbnd']['lat_inputs'];
			$long_inputs=$_SESSION['wizardbnd']['long_inputs'];
			$cpuwr=$_SESSION['wizardbnd']['cpuwr'];
			$cpucr=$_SESSION['wizardbnd']['cpucr'];
			$memwr=$_SESSION['wizardbnd']['memwr'];
			$memcr=$_SESSION['wizardbnd']['memcr'];
			$tempwr=$_SESSION['wizardbnd']['tempwr'];
			$tempcr=$_SESSION['wizardbnd']['tempcr'];
			
			$inbww=$_SESSION['wizardbnd']['inbww'];
			$inbwc=$_SESSION['wizardbnd']['inbwc'];
			$outbww=$_SESSION['wizardbnd']['outbww'];
			$outbwc=$_SESSION['wizardbnd']['outbwc'];
			$scaleSelector=$_SESSION['wizardbnd']['scaleSelector'];	

			$help=$_SESSION['wizardbnd']['help'];	
			$portNo=$_SESSION['wizardbnd']['portNo'];	
			$descr=$_SESSION['wizardbnd']['Descr'];
			
			$host_inputs1 = implode(',', $host_inputs);
			$IP = implode(',', $IP);
			$host_selector = implode(',', $host_selector);
			$contact_selector = implode(',', $contact_selector);
			$lat_inputs = implode(',', $lat_inputs);
			$long_inputs = implode(',', $long_inputs);
			$cpuwr = implode(',', $cpuwr);
			$cpucr = implode(',', $cpucr);
			$memwr = implode(',', $memwr);
			$memcr = implode(',', $memcr);
			$tempwr = implode(',', $tempwr);
			$tempcr = implode(',', $tempcr);

			$inbww=implode(',', $inbww);
			$inbwc=implode(',', $inbwc);
			$outbww=implode(',', $outbww);
			$outbwc=implode(',', $outbwc);
			$scaleSelector=implode(',', $scaleSelector);

			$help=implode(',', $help);
			$portNo=implode(',', $portNo);
			
			$myObj->host_inputs = $host_inputs1;
			$myObj->IP = $IP;
			$myObj->host_selector = $host_selector;
			$myObj->contact_selector = $contact_selector;
			$myObj->lat_inputs = $lat_inputs;
			$myObj->long_inputs = $long_inputs;
			$myObj->cpuwr = $cpuwr;
			$myObj->cpucr = $cpucr;
			$myObj->memwr = $memwr;
			$myObj->memcr = $memcr;
			$myObj->tempwr = $tempwr;
			$myObj->tempcr = $tempcr;
			$myObj->inbww = $inbww;
			$myObj->inbwc = $inbwc;
			$myObj->outbww = $outbww;
			$myObj->outbwc = $outbwc;
			$myObj->scaleSelector = $scaleSelector;
			$myObj->help = $help;
			$myObj->portNo = $portNo;
			$myJSON = json_encode($myObj);
			
			$printed=shell_exec("python3.6 /usr/local/nagiosxi/html/includes/configwizards/wizardbnd/start.py $myJSON");

			$ready=preg_replace('/<[^>]*>.*<\/[^>]*>|<[^>]*>|\\\\/', '', $printed);
		
			$i=0;
			foreach($host_inputs as &$value){
				if($i==0){
					$regmatch_host="{$value}";
				}else{
					$regmatch_host.="|{$value}";
				}
				$i++;
			}
			$output='<h5 class="ul">' . _("Results Log :") . '</h5> ';
			$service_count = 0;
			$host_count = 0;
			$check=0;			
			foreach($host_inputs as &$value){
				$hostResult= "~\"HostResult\": \"n{\"success\":\"Added {$value} to the system. Config imported but not yet applied.~";
				$pingResult = "~\"PingResult\": \"n{\"success\":\"Added {$value} :: Ping to the system. Config imported but not yet applied.~";
				$cpu = "~\"CPU\": \"n{\"success\":\"Added {$value} :: Check CPU to the system. Config imported but not yet applied.~";
				$mem = "~\"MEM\": \"n{\"success\":\"Added {$value} :: Check MEM to the system. Config imported but not yet applied.~";
				$psu = "~\"PSU\": \"n{\"success\":\"Added {$value} :: Check PSU to the system. Config imported but not yet applied.~";
				$temp = "~\"TEMP\": \"n{\"success\":\"Added {$value} :: Check TEMP to the system. Config imported but not yet applied.~";
				$fan = "~\"FAN\": \"n{\"success\":\"Added {$value} :: Check FAN to the system. Config imported but not yet applied.~";
				if(preg_match_all($hostResult,$ready,$output_array)){
					$output.="<br><br><br>HOST:<b> \"{$value}\"</b> is added to the system.<br>";
					$host_count++;							
				}else{
					$output.="<br><br><br>HOST:<b> \"{$value}\"</b> is <b>not</b> added to the system.<br>";
					$check++;
				}				

				if(preg_match_all($pingResult,$ready,$output_array)){
					$output.="<b>CHECK PING SERVICE</b>:successfuly added to \"{$value}\".<br>";
					$service_count++;
				}else{
					$output.="<b>CHECK PING SERVICE</b>:<b>couldn't</b> be added to \"{$value}\".<br>";
					$check++;
				}	

				if(preg_match_all($cpu,$ready,$output_array)){
					$output.="<b>CHECK CPU SERVICE</b>:successfuly added to \"{$value}\".<br>";
					$service_count++;
				}else{
					$output.="<b>CHECK CPU SERVICE</b>:<b>couldn't</b> be added to \"{$value}\".<br>";
					$check++;
				}	

				if(preg_match_all($mem,$ready,$output_array)){
					$output.="<b>CHECK MEM SERVICE</b>:successfuly added to \"{$value}\".<br>";
					$service_count++;
				}else{
					$output.="<b>CHECK MEM SERVICE</b>:<b>couldn't</b> be added to \"{$value}\".<br>";
					$check++;
				}	

				if(preg_match_all($psu,$ready,$output_array)){
					$output.="<b>CHECK PSU SERVICE</b>:successfuly added to \"{$value}\".<br>";
					$service_count++;
				}else{
					$output.="<b>CHECK PSU SERVICE</b>:<b>couldn't</b> be added to \"{$value}\".<br>";
					$check++;
				}	

				if(preg_match_all($temp,$ready,$output_array)){
					$output.="<b>CHECK TEMP SERVICE</b>:successfuly added to \"{$value}\".<br>";
					$service_count++;
				}else{
					$output.="<b>CHECK TEMP SERVICE</b>:<b>couldn't</b> be added to \"{$value}\".<br>";
					$check++;
				}	

				if(preg_match_all($fan,$ready,$output_array)){
					$output.="<b>CHECK FAN SERVICE</b>:successfuly added to \"{$value}\".<br><br>";
					$service_count++;
				}else{
					$output.="<b>CHECK FAN SERVICE</b>:<b>couldn't</b> be added to \"{$value}\".<br><br>";
					$check++;
				}		
				
				foreach($descr as &$description){
				$bandwidthResult = "~\"BandwidthResult\": \"n{\"success\":\"Added ({$regmatch_host}) :: {$description}~";
				$Status = "~\"StatusResult\": \"n{\"success\":\"Added ({$regmatch_host}) :: {$description}~";
				preg_match_all($bandwidthResult, $ready, $bwoutput_array);
				preg_match_all($Status, $ready, $status_output_array);

				if($bwoutput_array[1][0]==$value){
					$output.="<b>{$description} BANDWIDTH CHECK</b>:succesfully added to {$value}.<br>";
					$service_count++;
				}
				if($status_output_array[1][0]==$value){
					$output.="<b>{$description} STATUS CHECK</b>:succesfully added to {$value}.<br>";
					$service_count++;
				}					
				}
			}
			
			$applyConfig = '/{"success":"Apply config command has been sent to the backend."/';
			if(preg_match_all($applyConfig,$ready,$output_array)){
					$output.="<br><br><b>Apply config command has been sent to the backend succesfully.</b><br>";

				}else{
					$output.="<br><br><b>Apply config command has NOT been sent to the backend succesfully.</b><br>";
					$check++;
				}
			
			
			if($check!=0){
				print_r($printed);
			}			
		
			
			
			break;
	
		case CONFIGWIZARD_MODE_VALIDATESTAGE3DATA:
			@unlink('/usr/local/nagiosxi/html/config/uploads/FILE.xlsx');
			$server_ip=$_SERVER['SERVER_ADDR'];
			$par='Location: http:\/\/'.$server_ip.'/nagiosxi/config/monitoringwizard.php';
			header($par);
			die();
			break;
					
		

		case CONFIGWIZARD_MODE_GETSTAGE3OPTS:
			$outargs[CONFIGWIZARD_OVERRIDE_OPTIONS]=array(
				"max_check_attempts" => 15,
				"check_interval"        => 15,
				"retry_interval"        => 15,
				);
				
			 
			$result=CONFIGWIZARD_HIDE_OPTIONS;
				
				
			break;
			

				
            case CONFIGWIZARD_MODE_GETSTAGE4OPTS:	
				@unlink('/usr/local/nagiosxi/html/config/uploads/FILE.xlsx');
				$server_ip=$_SERVER['SERVER_ADDR'];
				$par='Location: http:\/\/'.$server_ip.'/nagiosxi/config/monitoringwizard.php';
				header($par);
				die();
					
				break;			

		 		 
		 		
			case CONFIGWIZARD_MODE_GETFINALSTAGEHTML:
				@unlink('/usr/local/nagiosxi/html/config/uploads/FILE.xlsx');
				$server_ip=$_SERVER['SERVER_ADDR'];
				$par='Location: http:\/\/'.$server_ip.'/nagiosxi/config/monitoringwizard.php';
				header($par);
				die();

			
			break;
		

		case CONFIGWIZARD_MODE_GETOBJECTS:

			
			break;
			
		default:
			break;			
		}
		
	return $output;
	}
	
function bwtable($data_array,$ip_array){
	$output='';
	$scale='';
	$scales_array=array("Kbps","Mbps","bps");
	$max = sizeof($data_array[9]);
	$new_array=$data_array[9];
	
	$tmp = array_count_values($data_array[9]);

  foreach($ip_array as &$ip){
	$i = 0; 
	$cnt = $tmp[$ip] + 1;
	$output.="<tbody>
    <tr>
      <th rowspan=\"{$cnt}\" scope=\"rowgroup\">{$ip}</th> ";
	while($i <= $max) {
		foreach ($scales_array as &$value){
			if($data_array[8][$i]==$value){
			$scale.="<option value={$value} selected=\"selected\">{$value}</option>";
		}else{
			$scale.="<option value={$value}>{$value}</option>";
			}
		}

		if($ip==$data_array[9][$i]){
		if(!$i==0){
			$output.="<tr>";
		}
			$output.="  
      <td>Port {$data_array[1][$i]}</td>
      <td>{$data_array[2][$i]}</td>";
	  if($data_array[8][$i]=='Mbps'){
		  $output.="
      <td>{$data_array[3][$i]} Mbps</td>";
	  }
	  elseif($data_array[8][$i]=='Kbps'){
		  $output.="
      <td>{$data_array[3][$i]} Kbps</td>";  	  
	  }
	  else{
		 $output.="
      <td>{$data_array[3][$i]} bps</td>";	
	  }
	  $output.="
	  <td>
	  <table>
	  <tbody>
	  <tr>
	  <td></td>
	  <td>Rate In:</td>
	  <td>Rate Out:</td>
	  <td></td>
	  <td>Rate In:</td>
	  <td>Rate Out:</td>	  
	  </tr>
	  <tr>
	  <td><label>Warning:</label></td>
	  <td><input type=\"text\" size=\"3\" name=\"inbww[]\" value=\"{$data_array[5][$i]}\" class=\"form-control condensed\"></td>
	  <td><input type=\"text\" size=\"3\" name=\"outbww[]\" value=\"{$data_array[4][$i]}\" class=\"form-control condensed\"></td>
	  <td><label>Critical:</label></td>
	  <td><input type=\"text\" size=\"3\" name=\"inbwc[]\" value=\"{$data_array[7][$i]}\" class=\"form-control condensed\"></td>
	  <td><input type=\"text\" size=\"3\" name=\"outbwc[]\" value=\"{$data_array[6][$i]}\" class=\"form-control condensed\"></td>
	  <td><select name=\"scaleSelector[]\" id=\"scaleSelector\" class=\"form-control\">{$scale}</select></td>
	  <td><input type=\"hidden\" id=\"help\" name=\"help[]\" value=\"{$ip}\"></td>
	  <td><input type=\"hidden\" id=\"portNo\" name=\"portNo[]\" value=\"{$data_array[1][$i]}\"></td>
	  </tr>
	  </tbody>
	  </table>
	  </td>
	  </tr>";
		if($i==$max){
			$output.='</tbody>';
		}
		
	}
	$scale='';
	$i++;
}
}

return $output;
}

function device_data($complete,$cleaner){

	$output='';
	$hostgroups='';
	$contactgroups='';
	$wranges='';
	$cranges='';
	
	for ($i = 5; $i <= 100; $i+=5) {
		if ($i==75){
			$wranges.="<option value={$i} selected=\"selected\">{$i}%</option>";
		}else{
		$wranges.="<option value={$i}>{$i}%</option>";
		}
	}
	
	for ($i = 5; $i <= 100; $i+=5) {
		if ($i==85){
			$cranges.="<option value={$i} selected=\"selected\">{$i}%</option>";
		}else{
			$cranges.="<option value={$i}>{$i}%</option>";
		}
	}

	
	foreach ($complete as &$value){	
		foreach ($cleaner[0] as &$value1){
			if (strval($value1)==strval($value[3])){
				$contactgroups.="<option value={$value1} selected=\"selected\">{$value1}</option>"; 
			}else{
				$contactgroups.="<option value={$value1}>{$value1}</option>"; 
			}
		
		}
		foreach ($cleaner[1] as &$value2){
			if (strval($value2)==strval($value[2])){
				$hostgroups.="<option value={$value2} selected=\"selected\">{$value2}</option>"; 
			}else{
				$hostgroups.="<option value={$value2}>{$value2}</option>"; 
			}
			
		}	
		$output.="<tr><td><input type=\"text\" name=\"host_inputs[]\" size=\"19\" value=\"{$value[0]}\"></td><td><input type=\"text\" size=\"12\" name=\"IP[]\" value=\"{$value[1]}\" readonly></td><td><select name=\"host-selector[]\" id=\"host-selector\" class=\"form-control\">{$hostgroups}</select></td><td><select name=\"contact-selector[]\" id=\"contact-selector\" class=\"form-control\">{$contactgroups}</select></td><td><input type=\"text\" size=\"10\" maxlength=\"10\" name=\"lat_inputs[]\" value=\"{$value[4]}\"></td><td><input type=\"text\" size=\"10\" maxlength=\"10\" name=\"long_inputs[]\" value=\"{$value[5]}\"></td><td><select name=\"cpuwr[]\" id=\"cpuwr\" class=\"form-control\">{$wranges}</select></td><td><select name=\"cpucr[]\" id=\"cpucr\" class=\"form-control\">{$cranges}</select></td><td><select name=\"memwr[]\" id=\"memwr\" class=\"form-control\">{$wranges}</select></td><td><select name=\"memcr[]\" id=\"memcr\" class=\"form-control\">{$cranges}</select></td><td><select name=\"tempwr[]\" id=\"tempwr\" class=\"form-control\">{$wranges}</select></td><td><select name=\"tempcr[]\" id=\"tempcr\" class=\"form-control\">{$cranges}</select></td></tr>";
	$hostgroups='';
	$contactgroups='';
	}
	return $output;
}	
	

	
function hosts_status($output_array,$output_array1,$output_array2,$output_array3){
	$output='';
	foreach ($output_array[0] as &$value) {
		if ($value!=''){
			$output.="<tr><td>{$value}</td><td align='center'>Successful</td><td align='center'>Successful</td></tr>";
		}
		
	}	
	foreach ($output_array1[0] as &$value) {
		if ($value!=''){
			$output.="<tr><td>{$value}</td><td align='center'>Successful</td><td align='center'><b>Not</b> successful</td></tr>";
		}
	}
	foreach ($output_array2[0] as &$value) {
		if ($value!=''){
			$output.="<tr><td>{$value}</td><td align='center'><b>Not</b> successful</td></tr>";
		}
	}
	foreach ($output_array3[0] as &$value) {
		if ($value!=''){
			$output.="<tr><td>{$value}</td><td align='center'><b>Not</b> successful</td><td align='center'><b>Not</b> successful</td></tr>";
		}		
	}	
	
	return $output;
}


?>