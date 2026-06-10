// ---------------- INIT ----------------
function init(){
    startClock();
    initChart();
    loadSensorData();
}

// ---------------- CLOCK ----------------
function startClock(){
    setInterval(() => {
        const now = new Date();
        document.getElementById("clock").innerText =
            now.toLocaleTimeString("en-IN");
    }, 1000);
}

// ---------------- CHART ----------------
let chart;

function initChart(){
    const ctx = document.getElementById("chart").getContext("2d");

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Moisture","Temp","Humidity"],
            datasets: [{
                label: "Sensor Data",
                data: [0,0,0],
                backgroundColor: ["#00ffcc","#00c3ff","#ffcc00"]
            }]
        }
    });
}

// ---------------- SENSOR ----------------
function loadSensorData(){
    setInterval(() => {

        // 🔥 TEST DATA (always working)
        const moisture = Math.floor(Math.random()*40)+40;
        const temperature = Math.floor(Math.random()*10)+25;
        const humidity = Math.floor(Math.random()*30)+50;

        document.getElementById("moisture").innerText = moisture + "%";
        document.getElementById("temperature").innerText = temperature + "°C";
        document.getElementById("humidity").innerText = humidity + "%";

        chart.data.datasets[0].data = [
            moisture,
            temperature,
            humidity
        ];
        chart.update();

        // alert
        let msg = "All conditions normal ✅";

        if(temperature > 35) msg = "High Temperature ⚠";
        else if(humidity < 40) msg = "Low Humidity ⚠";
        else if(moisture < 35) msg = "Low Moisture ⚠";

        document.getElementById("alertBox").innerText = msg;

    }, 3000);
}

async function loadWeather() {
    const city = document.getElementById("city").value.trim();

    if (!city) {
        alert("Enter city name");
        return;
    }

    const apiKey = "fc006ecc15d414af2305fd342465ad57";

    try {
        const res = await fetch(
            `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`
        );

        const data = await res.json();

        console.log("FULL RESPONSE:", data);

        // 🔥 REAL error show karo
        if (data.cod !== 200) {
            alert("Error: " + data.message);
            document.getElementById("weatherCond").innerText = data.message;
            return;
        }

        document.getElementById("weatherTemp").innerText = data.main.temp + " °C";
        document.getElementById("weatherHum").innerText = data.main.humidity + " %";
        document.getElementById("weatherWind").innerText = data.wind.speed + " m/s";
        document.getElementById("weatherCond").innerText = data.weather[0].main;

    } catch (error) {
        console.log(error);
        alert("Network error");
    }
}
// -------- CROP --------
async function predictCrop(){
    try{
        const res = await fetch("/predict", {
            method:"POST",
            headers: { "Content-Type":"application/json" },
            body: JSON.stringify({
                temperature: document.getElementById("tempInput").value,
                humidity: document.getElementById("humInput").value
            })
        });

        const data = await res.json();

        document.getElementById("aiCrop").innerText =
            "🌾 " + data.crop;

    }catch(e){
        console.log(e);
        alert("Backend error ❌");
    }
}


// -------- IMAGE --------
async function predictImage(){
    try{
        const fileInput = document.getElementById("imageInput");

        if(!fileInput.files[0]){
            alert("Select image ❗");
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        const res = await fetch("/predict-image", {
            method:"POST",
            body: formData
        });

        const data = await res.json();

        document.getElementById("imageResult").innerText =
            "Result: " + data.result;

    }catch(e){
        console.log(e);
        alert("Image prediction error ❌");
    }
}
function openAI(){
  document.getElementById("aiBox").style.display = "flex";
}

function closeAI(){
  document.getElementById("aiBox").style.display = "none";
}

function sendMessage(){
  let input = document.getElementById("aiInput");
  let msg = input.value.trim();

  if(msg === "") return;

  let chat = document.getElementById("chatBox");

  // user msg
  chat.innerHTML += `<div class="user-msg">${msg}</div>`;

  // typing
  chat.innerHTML += `<div id="typing" class="ai-msg typing">AI typing...</div>`;
  chat.scrollTop = chat.scrollHeight;

  fetch("http://127.0.0.1:5000/ask-ai", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({question: msg})
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("typing").remove();

    chat.innerHTML += `<div class="ai-msg">${data.answer}</div>`;
    chat.scrollTop = chat.scrollHeight;
  })
  .catch(() => {
    document.getElementById("typing").innerText = "Server error ❌";
  });

  input.value = "";
}

// ENTER key support
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("aiInput").addEventListener("keypress", function(e){
    if(e.key === "Enter"){
      sendMessage();
    }
  });
});