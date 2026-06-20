async function post(url, body={}){const r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});return r.json()}
function yn(v){return v?'<span class="danger">YES</span>':'<span class="ok">NO</span>'}
async function refresh(){try{let s=await (await fetch('/api/status')).json();let st=s.state;document.getElementById('banner').innerHTML=st.alarm?'🚨 ALARM ACTIVE':(st.stranger?'⚠️ Stranger found':'✅ Home safe');document.getElementById('security').innerHTML=`Armed: <b>${st.armed}</b> | Robot: <b>${st.motion}</b> | Trained: <b>${s.trained}</b>`;gas.innerHTML=yn(st.gas);fire.innerHTML=yn(st.fire);pir.innerHTML=yn(st.pir_motion);alarm.innerHTML=yn(st.alarm);people.innerHTML=(s.people||[]).map(p=>`<p>${p.name}: ${p.images} images</p>`).join('')||'No trained people yet.';let ev=await (await fetch('/api/events?limit=20')).json();events.innerHTML=(ev.events||[]).map(e=>`<div class="event"><b>${e.type}</b> ${new Date(e.ts*1000).toLocaleString()}<br>${e.message}</div>`).join('')}catch(e){document.getElementById('banner').innerText='Disconnected'}}
async function move(d){await post('/api/move/'+d);refresh()}
async function setSpeed(v){await post('/api/speed',{speed:v})}
async function arm(on){await post('/api/arm/'+(on?'on':'off'));refresh()}
async function alarm(on){await post('/api/alarm/'+(on?'on':'off'));refresh()}
async function capture(){let name=document.getElementById('person').value||'Owner';let r=await post('/api/capture',{name});trainStatus.innerText=r.ok?`Saved ${r.saved_count} image(s). Capture many angles.`:r.error;refresh()}
async function train(){let r=await post('/api/train');trainStatus.innerText=r.ok?`Trained: ${r.trained_people.join(', ')} with ${r.images} images`:r.error;refresh()}
setInterval(refresh,2000);refresh();if('serviceWorker' in navigator){navigator.serviceWorker.register('/static/sw.js')}
