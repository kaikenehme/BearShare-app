// Mock storage API using localStorage
function mockPostCommunity(formData) {
  return new Promise(resolve => {
    setTimeout(() => {
      const entry = Object.fromEntries(formData.entries());
      entry.id = Date.now();
      const list = JSON.parse(localStorage.getItem('communityList') || '[]');
      list.push(entry);
      localStorage.setItem('communityList', JSON.stringify(list));
      resolve({ success: true, data: { message: 'Operation successful (mocked)' } });
    }, 300);
  });
}

function mockGetCommunity() {
  return new Promise(resolve => {
    setTimeout(() => {
      const list = JSON.parse(localStorage.getItem('communityList') || '[]');
      resolve(list);
    }, 200);
  });
}
// auth-modal.js
const openBtns = document.querySelectorAll('#get-app-btn, #get-app-btn-2');
const modal   = document.getElementById('auth-modal');
const closeBtn= document.getElementById('modal-close');

const loginLink    = document.getElementById('show-login');
const registerLink = document.getElementById('show-register');
const loginForm    = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');

// 打开弹层
openBtns.forEach(btn => {
  btn.addEventListener('click', e => {
    e.preventDefault();
    modal.classList.remove('hidden');
  });
});

// 关闭弹层（× 或点击遮罩）
closeBtn.addEventListener('click', () => modal.classList.add('hidden'));
modal.addEventListener('click', e => {
  if (e.target === modal) modal.classList.add('hidden');
});

// 切换到登录
loginLink.addEventListener('click', e => {
  e.preventDefault();
  loginLink.classList.add('active');
  registerLink.classList.remove('active');
  loginForm.classList.remove('hidden');
  registerForm.classList.add('hidden');
});

// 切换到注册
registerLink.addEventListener('click', e => {
  e.preventDefault();
  registerLink.classList.add('active');
  loginLink.classList.remove('active');
  registerForm.classList.remove('hidden');
  loginForm.classList.add('hidden');
});

// // 表单提交示例（根据你的 API 改写）
// loginForm.addEventListener('submit', async e => {
//   e.preventDefault();
//   const data = new FormData(loginForm);
//   // TODO: 调用登录 API
//   // 如: await fetch('/api/auth/login', { method:'POST', body:data });
//   alert('Logging in: ' + data.get('username'));
//   // 登录成功后跳转到 App 下载页
//   // window.location.href = 'https://your.app.download/link';
// });

// registerForm.addEventListener('submit', async e => {
//   e.preventDefault();
//   const data = new FormData(registerForm);
//   if (data.get('password') !== data.get('confirmPassword')) {
//     alert('Passwords do not match!');
//     return;
//   }
//   // TODO: 调用注册 API
//   // 如: await fetch('/api/auth/register', { method:'POST', body:data });
//   alert('Registering: ' + data.get('firstName') + ' ' + data.get('lastName'));
//   // 注册成功后也可跳转
//   // window.location.href = 'https://your.app.download/link';
// });

// 假设这是你的 auth-modal.js 或者 community.js

loginForm.addEventListener('submit', async e => {
  e.preventDefault();
  const formData = new FormData(loginForm);
  // 如果登录接口也需要 student_number/uqcloud_zone_id，先 append
  formData.append('student_number', 's4863587');
  formData.append('uqcloud_zone_id', '7857996d');
  // Use mock storage API instead of real fetch
  const { success, data } = await mockPostCommunity(formData);
  if (success) {
    alert(data.message);
    loginForm.reset();
  } else {
    alert('Operation failed (mocked)');
  }
});

registerForm.addEventListener('submit', async e => {
  e.preventDefault();
  const formData = new FormData(registerForm);
  if (formData.get('password') !== formData.get('confirmPassword')) {
    alert('Passwords do not match!');
    return;
  }
  // 添加你需要的额外字段
  formData.append('student_number', 's4863587');
  formData.append('uqcloud_zone_id', '7857996d');
  // Use mock storage API instead of real fetch
  const { success, data } = await mockPostCommunity(formData);
  if (success) {
    alert(data.message);
    registerForm.reset();
  } else {
    alert('Operation failed (mocked)');
  }
});

// On page load, render stored entries in mock community
mockGetCommunity().then(list => {
  const container = document.getElementById('community-list');
  if (!container) return;
  list.forEach(member => {
    const card = document.createElement('div');
    card.className = 'card mb-3';
    card.innerHTML = `
      <div class="card-body">
        <h5 class="card-title">${member.username || member.name || 'Anonymous'}</h5>
        <p class="card-text">${member.message || 'No message provided.'}</p>
      </div>`;
    container.appendChild(card);
  });
});
