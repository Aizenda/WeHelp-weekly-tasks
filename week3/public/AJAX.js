
const burger = document.querySelector('.menu');
const fixed = document.querySelector('.fixed');

burger.addEventListener('click', () =>{
    fixed.classList.add("show");
});

fixed.addEventListener("click", (event) => {
    const rect = fixed.getBoundingClientRect();
    const isInTopRightCorner = event.clientX > rect.right - 50 && event.clientY < rect.top + 50;
    if (isInTopRightCorner) {
        fixed.classList.remove("show");
    }
});


const url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
fetch(url)
    .then((res) => res.json())
    .then((data) => {
        const regional_data = data["data"]["results"];
        const pattern = /https:\/\/.*?\.[Jj][Pp][Gg]/g;

        // 建立一組 Promise，讓每個資料處理都是非同步的
        const promises = regional_data.map((item, index) => {
            return new Promise((resolve) => {
                const title = item["stitle"];
                const imgSrc = item["filelist"].match(pattern)[0]; 
                if (imgSrc) {
                    if (index < 3) {
                        // 更新small-box
                        const promotionDiv = document.querySelectorAll('.small-boxes div')[index];
                        const imgElement = promotionDiv.querySelector('img');
                        imgElement.src = imgSrc;
                        imgElement.alt = " ";
                        const textElement = promotionDiv.querySelector('span');
                        if (textElement) {
                            textElement.textContent = title;
                        }
                    } else if (index < 13) {
                        // 更新big-box
                        const bigBoxDiv = document.querySelectorAll('.big-boxes div')[index - 3];
                        bigBoxDiv.style.backgroundImage = `url(${imgSrc})`;
                        const textElement = bigBoxDiv.querySelector('span');
                        if (textElement) {
                            textElement.textContent = title;
                        }
                    }
                }
                resolve(); // 完成此項處理
            });
        });

        // 等待所有 Promise 完成後再顯示內容
        Promise.all(promises).then(() => {
            document.getElementById('loading').style.display = "none";
            document.getElementById('main-content').style.display = "block";
        });
    })
    .catch((error) => {
        console.error("Error fetching data:", error);
    });
