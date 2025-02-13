# SQL指令與截圖

<h1 style="text-align: center;">Week 5 Task Summary</h1>

* ## MySQL Login Prerequisite
* ## Task 2: Create database and table in your MySQL server
	* [Q1: Create a new database named website](#q1-create-a-new-database-named-website)
	* [Q2: Create a new table named member, in the website database](#q2-create-a-new-table-named-member-in-the-website-database)

* ## Task 3: SQL CRUD
	* [Q1: INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data](#q1-insert-a-new-row-to-the-member-table-where-name-username-and-password-must-be-set-to-test-insert-additional-4-rows-with-arbitrary-data)
	* [Q2: SELECT all rows from the member table](#q2-select-all-rows-from-the-member-table)
	* [Q3: SELECT all rows from the member table, in descending order of time](#q3-select-all-rows-from-the-member-table-in-descending-order-of-time)
	* [Q4: SELECT total 3 rows, second to fourth, from the member table, in descending order of time](#q4-select-total-3-rows-second-to-fourth-from-the-member-table-in-descending-order-of-time)
	* [Q5: SELECT rows where username equals to test](#q5-select-rows-where-username-equals-to-test)
	* [Q6: SELECT rows where name includes the es keyword](#q6-select-rows-where-name-includes-the-es-keyword)
	* [Q7: SELECT rows where both username and password equal to test](#q7-select-rows-where-both-username-and-password-equal-to-test)
	* [Q8: UPDATE data in name column to test2 where username equals to test](#q8-update-data-in-name-column-to-test2-where-username-equals-to-test)

* ## Task 4: SQL Aggregation Functions
	* [Q1: SELECT how many rows from the member table](#q1-select-how-many-rows-from-the-member-table)
	* [Q2: SELECT the sum of follower_count of all the rows from the member table](#q2-select-the-sum-of-follower_count-of-all-the-rows-from-the-member-table)
	* [Q3: SELECT the average of follower_count of all the rows from the member table](#q3-select-the-average-of-follower_count-of-all-the-rows-from-the-member-table)
	* [Q4: SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table](#q4-select-the-average-of-follower_count-of-the-first-2-rows-in-descending-order-of-follower_count-from-the-member-table)

* ## Task 5: SQL JOIN
	* [Q1: Create a new table named message, in the website database](#q1-create-a-new-table-named-message-in-the-website-database)
	* [Q2: SELECT all messages, including sender names](#q2-select-all-messages-including-sender-names)
	* [Q3: SELECT all messages, including sender names, where sender username equals to test](#q3-select-all-messages-including-sender-names-where-sender-username-equals-to-test)
	* [Q4: Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test](#q4-use-select-sql-aggregation-functions-with-join-statement-get-the-average-like-count-of-messages-where-sender-username-equals-to-test)
	* [Q5: Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username](#q5-use-select-sql-aggregation-functions-with-join-statement-get-the-average-like-count-of-messages-group-by-sender-username)

# MySQL Login Prerequisite
### Q1: Use MySQL Login syntax  
	mysql -u [username] -p

### Q2: Key in password  

![前置](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/%E5%89%8D%E7%BD%AE.png)

# Task 2: Create database and table in your MySQL server
### Q1: Create a new database named website
* ### SQL code　＆　screenshots
		CREATE DATABASE website;

	![task2-1](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/2-1.png)
### Q2: Create a new table named member, in the website database

<table border="1" style="border-collapse: collapse;">
   <tr style="background-color: #34495e; color: white;">
       <th>Column Name</th>
       <th>Data Type</th>
       <th>Additional Settings</th>
       <th>Description</th>
   </tr>
   <tr>
       <td>id</td>
       <td>bigint</td>
       <td>primary key, auto increment</td>
       <td>Unique ID</td>
   </tr>
   <tr>
       <td>name</td>
       <td>varchar(255)</td>
       <td>not null</td>
       <td>Name</td>
   </tr>
   <tr>
       <td>username</td>
       <td>varchar(255)</td>
       <td>not null</td>
       <td>Username</td>
   </tr>
   <tr>
       <td>password</td>
       <td>varchar(255)</td>
       <td>not null</td>
       <td>Password</td>
   </tr>
   <tr>
       <td>follower_count</td>
       <td>int unsigned</td>
       <td>not null, default to 0</td>
       <td>Follower Count</td>
   </tr>
   <tr>
       <td>time</td>
       <td>datetime</td>
       <td>not null, default to current time</td>
       <td>Signup Time</td>
   </tr>
</table>  

<br/>

* ### SQL code　＆　screenshots 
		CREATE TABLE member (
				id BIGINT AUTO_INCREMENT,
				name VARCHAR(255) NOT NULL,
				username VARCHAR(255) NOT NULL,
				password VARCHAR(255) NOT NULL,
				follower_count INT UNSIGNED NOT NULL DEFAULT 0,
				time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
				PRIMARY KEY(id)
		);

	![task2-2](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/2-2.png)  

* ### Q2 derivative: How to view the member table structure?
	### syntax:
  
  ```
	DESC [table name];
	```  
	
# Task 3: SQL CRUD  
### Q1: INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.

* ### SQL code　&　screenshots　　
		INSERT INTO member (name, username, password)
		VALUES ('test', 'test', 'test');

	![task3-1](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/3-1.png) 
	```
	INSERT INTO member (name, username, password, follower_count)
	VALUES 
    ('Bob', 'bob123', 'bobpassword', 45),
    ('Mil', 'mil123', 'milpassword', 50),
    ('Jash', 'jash123', 'jashpassword', 55),
    ('Ailc', 'alic123', 'alicpassword', 60);
	```
### Q2: SELECT all rows from the member table.  
* ### SQL code　&　screenshots　　
		SELECT * FROM member;

	![task3-2](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/3-2.png)   

### Q3: SELECT all rows from the member table, in descending order of time.  
* ### SQL code　&　screenshots　　
		SELECT * FROM member
		ORDER BY time DESC;

	![task3-3](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/3-3.png)   

### Q4: SELECT total 3 rows, second to fourth, from the member table, in descending order of time.  
* ### SQL code　&　screenshots　　
		SELECT * FROM member
		ORDER BY time DESC
		LIMIT 1 , 3;

	![task3-4](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/3-4.png)   

### Q5: SELECT rows where username equals to test.  
* ### SQL code　&　screenshots　　
		SELECT * FROM member
		WHERE username='test';

	![task3-5](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/3-5.png)  


### Q6: SELECT rows where name includes the es keyword.  
* ### SQL code　&　screenshots　　
		SELECT * FROM member
		WHERE name LIIKE '%es%';

	![task3-6](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/3-6.png)  

### Q7: SELECT rows where both username and password equal to test.  
* ### SQL code　&　screenshots　　
		SELECT * FROM member
		WHERE name='test' AND password='test';

	![task3-7](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/3-7.png)  

### Q8: UPDATE data in name column to test2 where username equals to test. 
* ### SQL code　&　screenshots　　
		UPDATE member
		SET name='test'
		WHERE username='test';

	![task3-8](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/3-8.png) 

# Task 4: SQL Aggregation Functions  
### Q1: SELECT how many rows from the member table.
* ### SQL code　&　screenshots  
		SELECT COUNT(*) FROM member;
	
	![task4-1](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/4-1.png) 

### Q2: SELECT the sum of follower_count of all the rows from the member table.
* ### SQL code　&　screenshots  
		SELECT SUM(follower_count) AS follower_count FROM member;
	
	![task4-2](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/4-2.png) 

### Q3: SELECT the average of follower_count of all the rows from the member table.
* ### SQL code　&　screenshots  
		SELECT AVG(follower_count) AS follower_avg FROM member;
	
	![task4-3](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/4-3.png)   

### Q4: SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
* ### SQL code　&　screenshots  
		SELECT AVG(follower_count) AS top_2_follower 
		FROM (
			SELECT follower_count 
			FROM member
			ORDER BY follower_count DESC
			LIMIT 2
		) AS top_2;

	
	![task4-4](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/4-4.png)   

# Task 5: SQL JOIN
### Q1: Create a new table named message, in the website database.

<table border="1" style="border-collapse: collapse;">
   <tr style="background-color: #34495e; color: white;">
       <th>Column Name</th>
       <th>Data Type</th>
       <th>Additional Settings</th>
       <th>Description</th>
   </tr>
   <tr>
       <td>id</td>
       <td>bigint</td>
       <td>primary key, auto increment</td>
       <td>Unique ID</td>
   </tr>
   <tr>
       <td>member_id</td>
       <td>bigint</td>
       <td>not null,<br>foreign key refer to id column<br>in the member table</td>
       <td>Member ID for<br>Message Sender</td>
   </tr>
   <tr>
       <td>content</td>
       <td>varchar(255)</td>
       <td>not null</td>
       <td>Content</td>
   </tr>
   <tr>
       <td>like_count</td>
       <td>int unsigned</td>
       <td>not null, default to 0</td>
       <td>Like Count</td>
   </tr>
   <tr>
       <td>time</td>
       <td>datetime</td>
       <td>not null, default to current time</td>
       <td>Publish Time</td>
   </tr>
</table>

* ### SQL code　&　screenshots  
		CREATE TABLE message (
			id BIGINT AUTO_INCREMENT,
			member_id BIGINT NOT NULL,
			content VARCHAR(255) NOT NULL,
			like_count INT UNSIGNED NOT NULL DEFAULT 0,
			time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (id),
			FOREIGN KEY (member_id) REFERENCES member(id)
		);

	![task5-1](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/5-1.png)  

### Q2: SELECT all messages, including sender names. We have to JOIN the member table to get that.
* ### SQL code　&　screenshots  
		SELECT message.id, member.name AS name, message.content, message.like_count, message.time FROM message
		INNER JOIN member ON message.member_id = member.id;

	![task5-2](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/5-2.png)  

### Q3: SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.
* ### SQL code　&　screenshots 
 
		SELECT message.id, member.name AS name, message.content, message.like_count, message.time FROM message
		INNER JOIN member ON message.member_id = member.id 
		WHERE member.username = 'test';

	![task5-3](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/5-3.png)  


### Q4: SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.
* ### SQL code　&　screenshots 
 
		SELECT AVG(like_count) AS avg_like_count 
		FROM (
    		SELECT message.like_count 
    		FROM message
    		INNER JOIN member ON message.member_id = member.id
    		WHERE member.username = 'test'
		) AS username_test;

	![task5-4](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/5-4.png)  


### Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.
* ### SQL code　&　screenshots 
 
		SELECT member.name, AVG(message.like_count) AS avg_like_count FROM message 
		JOIN member ON message.member_id = member.id
		GROUP BY member.name;

	![task5-5](https://github.com/Aizenda/WeHelp-weekly-tasks/blob/main/week5/img/5-5-1.png)  
