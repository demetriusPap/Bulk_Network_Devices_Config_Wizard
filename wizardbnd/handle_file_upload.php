<?php
$target_path = "uploads/";
$file=$_FILES['afile'];
$file_name = $file['name'];
$file_ext = explode('.',$file_name);
$file_ext= strtolower(end($file_ext));
$file_name_new = 'FILE.'.$file_ext;
$targetPath  = $target_path . $file_name_new; 

$fileName = $_FILES['afile']['name'];
$fileType = $_FILES['afile']['type'];
$fileContent = file_get_contents($_FILES['afile']['tmp_name']);
$dataUrl = 'data:' . $fileType . ';base64,' . base64_encode($fileContent);
$json = json_encode(array(
  'name' => $fileName,
  'type' => $fileType,
  'dataUrl' => $dataUrl
));
if ($_FILES["afile"]["type"] == "application/xls" or $_FILES["afile"]["type"] == "application/vnd.ms-excel" or $_FILES["afile"]["type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"){
move_uploaded_file($_FILES['afile']['tmp_name'], $targetPath);
}
echo $json;
?>