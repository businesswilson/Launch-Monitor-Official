const video = document.getElementById('camera');
const speedDisplay = document.getElementById('speed');
const angleDisplay = document.getElementById('angle');
const canvas = document.getElementById('rangeCanvas');
const ctx = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  });

function startRecording() {
  const speed = (80 + Math.random() * 40).toFixed(1);
  const angle = (10 + Math.random() * 20).toFixed(1);

  speedDisplay.textContent = speed;
  angleDisplay.textContent = angle;

  drawTrajectory(speed, angle);
}

function drawTrajectory(speed, angle) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  ctx.moveTo(0, canvas.height);

  const factor = parseFloat(speed) * parseFloat(angle);
  for (let x = 0; x < canvas.width; x += 10) {
    const y = canvas.height - (Math.sin(x / 100) * factor / 10);
    ctx.lineTo(x, y);
  }

  ctx.strokeStyle = '#ffffff';
  ctx.stroke();
}
