<html>
	<head>
		<title>Hits Page</title>
		<meta charset="UTF-8">
	</head>
	<body>

		<h3> Hits and IP's on this page </h3>
			
		<?php
			$ipsFile = fopen("dps.txt", "a+") or fopen("dps.txt", "x+");
			
			$ip_elements = array(
				'HTTP_X_FORWARDED_FOR', 'HTTP_FORWARDED_FOR',
				'HTTP_X_FORWARDED', 'HTTP_FORWARDED',
				'HTTP_X_CLUSTER_CLIENT_IP', 'HTTP_CLUSTER_CLIENT_IP',
				'HTTP_X_CLIENT_IP', 'HTTP_CLIENT_IP',
				'REMOTE_ADDR'
			);
			
			foreach ( $ip_elements as $element ) {
				if(isset($_SERVER[$element])) {
					if ( !is_string($_SERVER[$element]) ) {
						continue;
					}
					$address_list = explode(',', $_SERVER[$element]);
					$address_list = array_map('trim', $address_list);
					
					foreach ( $address_list as $x ) {
						$ip_addresses[] = $x;
					}
				}
			}
			
			$detail = $ip_addresses[0];
			
			fwrite($ipsFile, "{$detail}\n");
			rewind($ipsFile);
			
			/*echo filesize("dps.txt");*/
			
 			echo "<table>";

			$count = -1;
			while(!feof($ipsFile)){
				$count = $count + 1;
				$currentip = fgets($ipsFile);
				echo "<tr><td> {$currentip} </td></tr>";
			}

			fclose($ipsFile);

			echo "<tr><td> Number of hits on this page: {$count} </td></tr>";

			echo "</table>";
		?>

	</body>
</html>
