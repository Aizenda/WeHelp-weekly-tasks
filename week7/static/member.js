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

	try {
		const response = await fetch(url, { method: "GET" });
		const data = await response.json();
		if (data.error) {
			throw new Error( data.message );
		};
		
		if (data.data === "null") {
			result.textContent = '找不到會員資料';
		} else {
			result.textContent = `${ data.data.name } (${ data.data.username })`;
		};

	} catch(error){
		window.location.href = `/error?message=${ data.message }`;
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

	try {

		const response = await fetch(url, {
			method : "PATCH", 
			headers : header,
			body : JSON.stringify( { "name" : newName } )
		});

		const data = await response.json();
		if (data.status_code === 400) {

			window.location.href = `/error?message=${ data.message }`;

		} else if(data.status_code === 500){

			window.location.href = `/error?message=${ data.message }`;

		}else if(data.ok){

			displayName.textContent =  `歡迎 ${ data.response_name } 登入系統~~`;
			status.textContent = data.message;

		};
		
	} catch(error) {

		window.location.href = "/error?message=發生錯誤，請稍後再試";
		console.error("請求失敗:", error);

	};
};
