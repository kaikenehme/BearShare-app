// 依赖：GSAP（在 HTML 里单独引入 gsap.js）

const photobox = {
    container: document.querySelector(".photos"),
    img_data: [],
    container_width: 0,
    container_height: 0,
    photo_width: 0,
    photo_height: 0,
    if_movable: false,
    mouse_x: 0,
    mouse_y: 0,
    standard_width: 1440,
    scale_nums: 1,
  
    init() {
      this.resize();
      window.addEventListener("resize", () => this.resize());
  
      this.container.addEventListener("mousedown", (event) => {
        this.if_movable = true;
        this.mouse_x = event.clientX;
        this.mouse_y = event.clientY;
      });
      this.container.addEventListener("mouseup", () => {
        this.if_movable = false;
      });
      this.container.addEventListener("mouseleave", () => {
        this.if_movable = false;
      });
      this.container.addEventListener("mousemove", (event) => {
        this.move(event.clientX, event.clientY);
      });
    },
  
    resize() {
      const imgs = Array.from(document.querySelectorAll(".photos_line_photo"));
      this.container_width = this.container.offsetWidth;
      this.container_height = this.container.offsetHeight;
      this.photo_width = imgs[0].offsetWidth;
      this.photo_height = imgs[0].offsetHeight;
      this.scale_nums = document.body.offsetWidth / this.standard_width;
  
      // 缩放整个容器
      this.container.style.transform = `scale(${this.scale_nums})`;
  
      // 重置所有图片位置
      gsap.to(imgs, {
        transform: `translate(0,0)`,
        duration: 0,
        ease: "power4.out",
      });
  
      // 记录初始数据
      this.img_data = imgs.map((img) => ({
        node: img,
        x: img.offsetLeft,
        y: img.offsetTop,
        mov_x: 0,
        mov_y: 0,
        ani: null,
      }));
    },
  
    move(x, y) {
      if (!this.if_movable) return;
  
      const dx = (x - this.mouse_x) / this.scale_nums;
      const dy = (y - this.mouse_y) / this.scale_nums;
  
      this.img_data.forEach((img) => {
        let duration = 1;
        img.mov_x += dx;
        if (img.x + img.mov_x > this.container_width) {
          img.mov_x -= this.container_width;
          duration = 0;
        }
        if (img.x + img.mov_x < -this.photo_width) {
          img.mov_x += this.container_width;
          duration = 0;
        }
  
        img.mov_y += dy;
        if (img.y + img.mov_y > this.container_height) {
          img.mov_y -= this.container_height;
          duration = 0;
        }
        if (img.y + img.mov_y < -this.photo_height) {
          img.mov_y += this.container_height;
          duration = 0;
        }
  
        // 杀掉旧动画，启动新动画
        if (img.ani) img.ani.kill();
        img.ani = gsap.to(img.node, {
          transform: `translate(${img.mov_x}px,${img.mov_y}px)`,
          duration: duration,
          ease: "power4.out",
        });
      });
  
      this.mouse_x = x;
      this.mouse_y = y;
    },
  };
  
  document.addEventListener("DOMContentLoaded", () => {
    photobox.init();
  });