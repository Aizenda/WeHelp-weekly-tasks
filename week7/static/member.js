//留言確認
function validateMessage(){
	const messageInput = document.getElementById("message"); 
	const messageValue = messageInput.value.trim(); 

	if (!messageValue) {
			alert("請輸入留言，不能為空!!");
			return false; 
	};

	return confirm("確定送出留言？");
}

function confirmDelete() {
	return confirm("確定要刪除這則留言嗎？");
	}

// 會員查詢
async function searchMember(){
	const username = document.getElementById("username").value.trim();
	const result = document.getElementById("result");
	if (!username){
		alert("姓名不能為空")
		return
	};

	const url = `http://127.0.0.1:8000/api/member?username=${username}`;

	const response = await fetch(url, { method: "GET" });
	const data = await response.json();
	if (!data.data) {
		result.textContent = '找不到會員資料';
	} else {
		result.textContent = `${ data.data.name } (${ data.data.username })`;
	};

};

// 姓名更新
async function updateName(){
	const newName = document.getElementById("newName").value;
	const displayName = document.getElementById("displayName");
	const status = document.getElementById("status");
	if(!newName){
		alert("請輸入要更新的姓名，不可為空!!");
		return
	};

	const url = "http://127.0.0.1:8000/api/member"
	const header = {
		"Content-Type" : "application/json"
	}

	const response = await fetch(url, {
		method : "PATCH", 
		headers : header,
		body : JSON.stringify( { "name" : newName } )
	});

	const data = await response.json();
	if (!data.ok) {
		status.textContent = "更新失敗，姓名與前一次相同"
		return
	}
	displayName.textContent  = `歡迎${newName}登入系統~~`
	status.textContent = "更新成功"

};
