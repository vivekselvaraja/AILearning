"""
Snake Game — Streamlit app:
 - Start Game button (game does not start until pressed)
 - Pause and Resume buttons (separate)
 - Restart button
 - Wall collisions => Game Over (no wrapping)
 - Centered yellow "GAME OVER" text only when collision happens
 - Dashboard white background + black text
 - Title styled with neon pink/purple gradient + white text
 - Updated: Pixel font, larger play area, red apple food, green apple snake head
"""
import streamlit as st
import streamlit.components.v1 as components

# ---------------- Streamlit page ----------------
st.set_page_config(page_title="Snake — Neon", layout="centered")

# Dashboard styling
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #FFFFFF !important;
        color: black !important;
    }
    h1.custom-title {
        background: linear-gradient(90deg, #ff0080, #8e2de2);
        color: white !important;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown(
    '<h1 class="custom-title">Snake Game</h1>',
    unsafe_allow_html=True
)

st.markdown("🎮 Press **Start** to begin. Use arrow keys or on-screen buttons to play. Hitting the wall ends the game.")

# ========== Game HTML / JS ==========
game_html = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
:root{--bg:#FFFFFF;--neon:#00f5ff;--accent:#ffd400;--snake-body:#35c56f;}
html,body{height:100%;margin:0;background:var(--bg);font-family:'Press Start 2P', cursive;}
.wrap{display:flex;flex-direction:column;align-items:center;padding:12px;}
.panel{background:rgba(0,0,0,0.05); padding:12px; border-radius:12px; box-shadow:0 8px 30px rgba(0,0,0,0.1);}
canvas{background:transparent;border-radius:10px; display:block;}
.ui{margin-top:10px; display:flex; gap:10px; align-items:center; justify-content:center; flex-wrap:wrap; font-size:12px;}
.btn{background:linear-gradient(90deg,#e0e0e0,#f5f5f5); color:black; padding:8px 12px; border-radius:10px; cursor:pointer; border:0; box-shadow:0 2px 4px rgba(0,0,0,0.1); font-family:'Press Start 2P', cursive; font-size:10px;}
.score{font-weight:700; color:var(--neon); font-size:12px;}
.overlay {
  position:absolute;
  left:50%;
  top:50%;
  transform:translate(-50%,-50%);
  font-size: 36px;
  font-weight: 800;
  color: #ffd400;
  text-shadow: 0 4px 18px rgba(0,0,0,0.6);
  pointer-events: none;
  display: none;
  font-family:'Press Start 2P', cursive;
}
.mobile-controls {display: none;}
@media (max-width:700px){ .mobile-controls{display:flex; flex-wrap:wrap; justify-content:center; gap:10px;} .dir {font-size:24px; padding:10px; background:#f0f0f0; border-radius:8px;} }
</style>
</head>
<body>
<div class="wrap" style="position:relative;">
  <div class="panel">
    <canvas id="c" width="600" height="600"></canvas>
    <div class="ui">
      <div class="score">Score: <span id="score">0</span></div>
      <button class="btn" id="startBtn">Start Game</button>
      <button class="btn" id="pauseBtn" disabled>Pause</button>
      <button class="btn" id="resumeBtn" disabled>Resume</button>
      <button class="btn" id="restartBtn" disabled>Restart</button>
    </div>
    <div class="mobile-controls">
      <div class="dir" id="up">▲</div>
      <div class="dir" id="left">◄</div>
      <div class="dir" id="down">▼</div>
      <div class="dir" id="right">►</div>
    </div>
  </div>
  <div id="overlay" class="overlay">Game Over</div>
</div>

<script>
(() => {
  let audioCtx = null;
  function ensureAudio(){ if(!audioCtx){ try{ audioCtx = new (window.AudioContext||window.webkitAudioContext)(); }catch(e){} } }
  function playBeep(f,t='sine',d=0.08,v=0.12,dec=0.12){ try{ ensureAudio(); if(!audioCtx)return; const o=audioCtx.createOscillator(); const g=audioCtx.createGain(); o.type=t; o.frequency.value=f; g.gain.value=v; o.connect(g); g.connect(audioCtx.destination); o.start(); g.gain.exponentialRampToValueAtTime(0.0001,audioCtx.currentTime+d+dec); setTimeout(()=>{try{o.stop()}catch(e){}},(d+dec)*1000+20);}catch(e){} }
  function playEat(){ playBeep(840,'triangle',0.1,0.12,0.06); setTimeout(()=>playBeep(1200,'sine',0.05,0.08,0.04),80); }
  function playGameOver(){ playBeep(160,'sawtooth',0.32,0.18,0.2); setTimeout(()=>playBeep(120,'sawtooth',0.26,0.09,0.18),120); }

  const canvas=document.getElementById('c'), ctx=canvas.getContext('2d');
  const overlay=document.getElementById('overlay');
  const scoreEl=document.getElementById('score');
  const startBtn=document.getElementById('startBtn');
  const pauseBtn=document.getElementById('pauseBtn');
  const resumeBtn=document.getElementById('resumeBtn');
  const restartBtn=document.getElementById('restartBtn');

  const GRID=20, CELL=Math.floor(canvas.width/GRID);
  let speed=8;
  let snake, dir, nextDir, food, running=false, paused=false, score=0, tickTimer=null, gameOver=false;

  // Load images
  const redApple = new Image();
  redApple.src = 'https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg';
  const greenApple = new Image();
  greenApple.src = 'https://upload.wikimedia.org/wikipedia/commons/5/5b/Granny_smith.jpg';

  function resetGameState(){
    snake=[{x:Math.floor(GRID/2),y:Math.floor(GRID/2)}];
    snake.push({x:snake[0].x-1,y:snake[0].y});
    snake.push({x:snake[0].x-2,y:snake[0].y});
    dir={x:1,y:0}; nextDir={x:1,y:0};
    score=0; speed=8; placeFood();
    running=false; paused=false; gameOver=false;
    overlay.style.display='none';
    updateScore();
    pauseBtn.disabled=true; resumeBtn.disabled=true; restartBtn.disabled=true; startBtn.disabled=false;
  }

  function placeFood(){ while(true){ const x=Math.floor(Math.random()*GRID), y=Math.floor(Math.random()*GRID); if(!snake.some(s=>s.x===x&&s.y===y)){ food={x,y}; return; } } }

  function updateScore(){ scoreEl.textContent = score; }

  function drawBackground(){
    ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0,0,canvas.width,canvas.height);
    for(let i=0;i<GRID;i++){ const x=i*CELL; ctx.fillStyle = (i%2===0)?'rgba(0,0,0,0.02)':'rgba(0,0,0,0.04)'; ctx.fillRect(x,0,CELL,canvas.height); }
    ctx.lineWidth = 4; ctx.strokeStyle = '#ffd400'; ctx.strokeRect(2,2,canvas.width-4,canvas.height-4);
  }

  function drawCell(x,y,inset=0,fill='#fff'){ const px=x*CELL,py=y*CELL,pad=Math.floor(inset*CELL); ctx.fillStyle=fill; ctx.beginPath(); if(ctx.roundRect) ctx.roundRect(px+pad,py+pad,CELL-2*pad,CELL-2*pad,6); else ctx.fillRect(px+pad,py+pad,CELL-2*pad,CELL-2*pad); ctx.fill(); }

  if (!CanvasRenderingContext2D.prototype.roundRect){
    CanvasRenderingContext2D.prototype.roundRect = function(x,y,w,h,r){
      if (typeof r === 'number') r = {tl:r,tr:r,br:r,bl:r};
      else r = Object.assign({tl:0,tr:0,br:0,bl:0}, r);
      this.beginPath();
      this.moveTo(x + r.tl, y);
      this.arcTo(x + w, y, x + w, y + h, r.tr);
      this.arcTo(x + w, y + h, x, y + h, r.br);
      this.arcTo(x, y + h, x, y, r.bl);
      this.arcTo(x, y, x + w, y, r.tl);
      this.closePath();
    };
  }

  function draw(){
    drawBackground();
    // Food (red apple)
    if (redApple.complete) {
      ctx.drawImage(redApple, food.x * CELL, food.y * CELL, CELL, CELL);
    } else {
      // Fallback if image not loaded
      ctx.shadowColor = 'rgba(255,94,126,0.66)';
      ctx.shadowBlur = 12;
      drawCell(food.x, food.y, 0.18, '#ff5e7e');
      ctx.shadowBlur = 0;
    }
    // Snake
    for(let i=0;i<snake.length;i++){
      const s = snake[i];
      if(i===0){
        // Head (green apple)
        if (greenApple.complete) {
          ctx.drawImage(greenApple, s.x * CELL, s.y * CELL, CELL, CELL);
        } else {
          // Fallback
          ctx.shadowColor = 'rgba(142,252,138,0.9)';
          ctx.shadowBlur = 14;
          drawCell(s.x, s.y, 0.12, '#8aff8a');
          ctx.shadowBlur = 0;
        }
      } else {
        // Body
        drawCell(s.x, s.y, 0.18, '#35c56f');
      }
    }
    overlay.style.display = gameOver ? 'block' : 'none';
  }

  function step(){
    if(!running || paused) return;
    if (nextDir.x !== -dir.x || nextDir.y !== -dir.y) dir = nextDir;
    const head = { x: snake[0].x + dir.x, y: snake[0].y + dir.y };

    if (head.x < 0 || head.x >= GRID || head.y < 0 || head.y >= GRID) {
      running = false; paused = false; gameOver = true; playGameOver();
      pauseBtn.disabled = true; resumeBtn.disabled = true; startBtn.disabled = false; restartBtn.disabled = false;
      return;
    }

    snake.unshift(head);
    let ate = false;
    if (head.x === food.x && head.y === food.y) {
      ate = true;
      score += 1; updateScore(); playEat(); placeFood();
      if (score % 5 === 0 && speed < 20) { speed += 1; restartLoop(); }
    } else {
      snake.pop();
    }

    for(let i = 1; i < snake.length; i++){
      if(snake[i].x === head.x && snake[i].y === head.y){
        running = false; paused = false; gameOver = true; playGameOver();
        pauseBtn.disabled = true; resumeBtn.disabled = true; startBtn.disabled = false; restartBtn.disabled = false;
        return;
      }
    }
  }

  function startLoop(){ if(tickTimer) clearInterval(tickTimer); tickTimer = setInterval(()=>{ step(); draw(); }, 1000 / speed); }
  function restartLoop(){ if(tickTimer) clearInterval(tickTimer); tickTimer = setInterval(()=>{ step(); draw(); }, 1000 / speed); }

  // Controls
  startBtn.addEventListener('click', () => {
    resetGameState();
    running = true; paused = false; gameOver = false;
    overlay.style.display = 'none';
    startBtn.disabled = true;
    pauseBtn.disabled = false;
    resumeBtn.disabled = true;
    restartBtn.disabled = false;
    startLoop();
  });

  pauseBtn.addEventListener('click', () => {
    if (!running || gameOver) return;
    paused = true;
    pauseBtn.disabled = true;
    resumeBtn.disabled = false;
  });

  resumeBtn.addEventListener('click', () => {
    if (!running || gameOver) return;
    paused = false;
    pauseBtn.disabled = false;
    resumeBtn.disabled = true;
  });

  restartBtn.addEventListener('click', () => {
    resetGameState();
    running = true; paused = false; gameOver = false;
    overlay.style.display = 'none';
    startBtn.disabled = true;
    pauseBtn.disabled = false;
    resumeBtn.disabled = true;
    restartBtn.disabled = false;
    startLoop();
  });

  // Keyboard
  window.addEventListener('keydown', (e) => {
    ensureAudio();
    if (!running || paused || gameOver) return;
    const key = e.key.toLowerCase();
    if (key === 'arrowup' || key === 'w') nextDir = { x: 0, y: -1 };
    else if (key === 'arrowdown' || key === 's') nextDir = { x: 0, y: 1 };
    else if (key === 'arrowleft' || key === 'a') nextDir = { x: -1, y: 0 };
    else if (key === 'arrowright' || key === 'd') nextDir = { x: 1, y: 0 };
  });

  // Mobile buttons
  ['up','down','left','right'].forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    const setDir = () => {
      if (gameOver || !running || paused) return;
      if (id === 'up') nextDir = { x: 0, y: -1 };
      if (id === 'down') nextDir = { x: 0, y: 1 };
      if (id === 'left') nextDir = { x: -1, y: 0 };
      if (id === 'right') nextDir = { x: 1, y: 0 };
    };
    el.addEventListener('touchstart', (ev) => { ev.preventDefault(); setDir(); });
    el.addEventListener('mousedown', (ev) => { ev.preventDefault(); setDir(); });
  });

  // Init
  resetGameState();
  draw();
})();
</script>
</body>
</html>
"""

# Embed the game
components.html(game_html, height=860, scrolling=True)
