
  const track       = document.querySelector('.card-carousel__track');
  const progressBar = document.querySelector('.card-carousel__progress');
  const fill        = document.querySelector('.card-carousel__progress-fill');
  const koala       = document.querySelector('.card-carousel__koala');

  function updateProgress() {
    const { scrollLeft, scrollWidth, clientWidth } = track;
    const ratio = scrollLeft / (scrollWidth - clientWidth);

    // 更新进度填充宽度
    fill.style.width = (ratio * 100) + '%';

    // 计算考拉水平位置
    const maxX = progressBar.clientWidth;
    koala.style.setProperty('--x', `${ratio * maxX}px`);
  }

  track.addEventListener('scroll', updateProgress);
  window.addEventListener('load', updateProgress);
