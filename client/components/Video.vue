<template>
    <div id="app">
      <div class="container">
        <div class="video-reaction-modal-backdrop flex items-center justify-center" v-if="showModal" @click.self="dismissModal">
          <div class="video-reaction-modal">
            <div class="video-reaction-modal-header">Reaction</div>
            <textarea class="video-reaction-modal-text" name="" id="" cols="30" rows="5" v-model="reactionText"></textarea>
            <button class="btn btn-primary w-full ml-auto" @click="submitReaction">{{ selectedEmoji.text }}</button>
          </div>
        </div>
        <div class="video-container" @mouseenter="mouseEnterVideo" @mouseleave="mouseLeaveVideo" ref="videoContainer">
          <video class="video" :poster="options.poster" @click="screenClick" ref="video">
            <source v-for="source in sources" :src="source.src" :type="source.type" :key="source.src" />
          </video>
          <div class="video-reaction-specific" :style="reactionStyle" ref="specific">
            <div class="video-reaction-specific-option" ref="specific" v-for="emoji of reaction.options" :key="emoji.id" @mouseenter="reactionMouseEnter" @mouseleave="reactionMouseLeave" @click="selectedReaction(emoji)">
              {{ emoji.text }}
            </div>
          </div>
          <div class="video-reaction-bar" :class="{'video-reaction-bar-hidden': !state.contrlShow}">
            <div class="video-reaction-options" :class="{'video-reaction-options-visible': reaction.showOptions}">
              <div class="video-reaction-col">
                <div v-if="category['NHI'] && category['NHI'].length > 0" class="video-reaction-option" :class="{'video-reaction-option-active': reaction.active['NHI']}" @mouseover="reactionOptionHover($event, 'NHI')" @mouseenter="reactionMouseEnter" @mouseleave="reactionMouseLeave">
                  {{ category['NHI'].length > 1 ? category['NHI'][1]['text'] : category['NHI'][0]['text'] }}
                </div>
                <div v-if="category['NLI'] && category['NLI'].length > 0" class="video-reaction-option" :class="{'video-reaction-option-active': reaction.active['NLI']}" @mouseover="reactionOptionHover($event, 'NLI')" @mouseenter="reactionMouseEnter" @mouseleave="reactionMouseLeave">
                  {{ category['NLI'].length > 1 ? category['NLI'][1]['text'] : category['NLI'][0]['text'] }}
                </div>
                <div v-if="category['PLI'] && category['PLI'].length > 0" class="video-reaction-option" :class="{'video-reaction-option-active': reaction.active['PLI']}" @mouseover="reactionOptionHover($event, 'PLI')" @mouseenter="reactionMouseEnter" @mouseleave="reactionMouseLeave">
                  {{ category['PLI'].length > 1 ? category['PLI'][1]['text'] : category['PLI'][0]['text'] }}
                </div>
                <div v-if="category['PHI'] && category['PHI'].length > 0" class="video-reaction-option" :class="{'video-reaction-option-active': reaction.active['PHI']}" @mouseover="reactionOptionHover($event, 'PHI')" @mouseenter="reactionMouseEnter" @mouseleave="reactionMouseLeave">
                  {{ category['PHI'].length > 1 ? category['PHI'][1]['text'] : category['PHI'][0]['text'] }}
                </div>
              </div>
            </div>
            <div class="video-reaction-btn" @click="toggleReaction" @mouseenter="reactionMouseEnter" @mouseleave="reactionMouseLeave">
              😀
            </div>
          </div>
          <transition name="fade">
            <div class="video-content" v-show="state.contrlShow">
              <button class="video-play-btn" @click="play">
                <svg class="video-play-btn-icon" v-show="!state.playing" viewBox="0 0 47 57" version="1.1" xmlns="http://www.w3.org/2000/svg">
                  <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                    <polygon id="Triangle-1" stroke="#FFFFFF" fill="#FFFFFF" points="1 56 1 1 47 28.5"></polygon>
                  </g>
                </svg>
                <svg class="video-play-btn-icon" v-show="state.playing" viewBox="0 0 15 22" version="1.1" xmlns="http://www.w3.org/2000/svg">
                  <defs>
                    <path d="M0,0.979149244 L5,0.979149244 L5,22 L0,22 L0,0.979149244 Z M10,0.979149244 L15,0.979149244 L15,22 L10,22 L10,0.979149244 Z" id="path-1"></path>
                    <mask id="mask-2" maskContentUnits="userSpaceOnUse" maskUnits="objectBoundingBox" x="0" y="0" width="15" height="21.0208508" fill="white">
                        <use xlink:href="#path-1"></use>
                    </mask>
                  </defs>
                  <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                    <use id="Combined-Shape" stroke="#FFFFFF" mask="url(#mask-2)" stroke-width="2" fill="#FFFFFF" xlink:href="#path-1"></use>
                  </g>
                </svg>
              </button>
              <div class="video-progress-bar" ref="progressBar">
                <div class="video-progress-rail" @click="slideClick">
                  <div class="video-progress-rail-inner" :style="{ 'width': `${video.pos.current}%`}"></div>
                </div>
              </div>
              <div class="video-control-time">
                  <span class="video-control-time-text">{{video.displayTime}}</span>
              </div>
              <div class="video-control-volume-box">
              <button class="video-play-btn" @click="volMuted">
                <svg class="video-control-volume-btn-icon" viewBox="0 0 41 44" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                  <defs>
                      <path d="M8.61522369,12 L20,0.615223689 L20,37.3847763 L8.61522369,26 L1.99201702,26 C0.891856397,26 0,25.1029399 0,23.9941413 L0,14.0058587 C0,12.8980535 0.900176167,12 1.99201702,12 L8.61522369,12 L8.61522369,12 Z" id="cov-vol"></path>
                  </defs>
                  <g id="Page-1" stroke="none" stroke-width="2" fill="none" fill-rule="evenodd">
                    <g id="vol" transform="translate(2.000000, 3.000000)">
                      <g id="cov-vol-icon">
                        <g id="Combined-Shape-Clipped">
                          <path v-show="volume.percent > 1 && !volume.muted" d="M25,29.5538997 C28.4589093,27.6757536 31.2629093,23.2984641 31.2629093,19.7769499 C31.2629093,16.2554357 28.4589093,11.8781461 25,10" id="vol-range-2" stroke="#FFFFFF"></path>
                          <path v-show="volume.percent > 70 && !volume.muted" d="M28,35.5538997 C33.5816016,32.5231573 38.1063837,25.4595762 38.1063837,19.7769499 C38.1063837,14.0943235 33.5816016,7.03074247 28,4" id="vol-range-2" stroke="#FFFFFF"></path>
                          <mask id="mask-2" fill="white">
                            <use xlink:href="#cov-vol"></use>
                          </mask>
                          <use id="vol-path" stroke="#FFFFFF" stroke-width="3" xlink:href="#cov-vol"></use>
                          <g id="Combined-Shape" mask="url(#mask-2)" stroke="#FFFFFF" stroke-width="2" fill="#FFFFFF">
                            <path d="M8.61522369,12 L20,0.615223689 L20,37.3847763 L8.61522369,26 L1.99201702,26 C0.891856397,26 0,25.1029399 0,23.9941413 L0,14.0058587 C0,12.8980535 0.900176167,12 1.99201702,12 L8.61522369,12 L8.61522369,12 Z" id="cov-vol"></path>
                          </g>
                        </g>
                      </g>
                    </g>
                  </g>
                </svg>
              </button>
                <div class="video-volume-slider" @click="volSlideClick" @mousedown="volMove">
                  <div class="video-volume-rail">
                    <div class="video-volume-rail-inner" :style="{ 'transform': `translate3d(${-volume.pos.current}px, 0, 0)`}"></div>
                  </div>
                </div>
              </div>
              <button class="video-play-btn" @click="fullScreen">
                <svg class="video-control-volume-btn-icon" viewBox="0 0 33 33" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                  <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                    <path d="M31.1682064,22 L31.1682064,31.0073537 L22,31.0073537 M22,1 L31.0073537,1 L31.0073537,10.1682064 M1,10.0073537 L1,1 L10.1682064,1 M10.0073537,31.1682064 L1,31.1682064 L1,22" id="Combined-Shape" stroke="#FFFFFF" stroke-width="2"></path>
                  </g>
                </svg>
              </button>
            </div>
          </transition>
        </div>
      </div>
    </div>
</template>
<script lang="ts">
import Vue from 'vue'
import Api from '~/services/api';

const getMousePosition = function (e: MouseEvent, type = "x") {
  if (type === "x") {
    return e.pageX;
  }
  return e.pageY;
};

const pad = (val: number) => {
  val = Math.floor(val);
  if (val < 10) {
    return "0" + val;
  }
  return val + "";
};

const timeParse = (sec: number) => {
  let min = 0;
  min = Math.floor(sec / 60);
  sec = sec - min * 60;
  return pad(min) + ":" + pad(sec);
};

export default Vue.extend({
  props: {
    sources: Array,
    options: {
      type: Object,
      default() {
        return {
          autoplay: false,
          volume: 0.9,
          poster: "",
        };
      },
    },
    videoId: Number,
    category: {
      type: Object,
      default() {
        return {};
      }
    },
  },
  data() {
    return {
      lastTime: '',
      reactionText: '',
      selectedEmoji: {} as {id: string, text: string},
      showModal: false,
      $video: null as HTMLVideoElement|null,
      video: {
        $videoSlider: null as Element|null,
        len: 0,
        current: 0,
        loaded: 0,
        moving: false,
        displayTime: "00:00",
        pos: {
          start: 0,
          width: 0,
          innerWidth: 0,
          current: 0,
        },
      },
      volume: {
        $volBox: null as Element|null,
        muted: false,
        percent: 60,
        moving: false,
        pos: {
          start: 0,
          width: 0,
          innerWidth: 0,
          current: 0,
        },
      },
      player: {
        $player: null as Element|null,
        pos: null as DOMRect|null,
      },
      tmp: {
        contrlHideTimer: null as NodeJS.Timeout|null,
        reactionHideTimer: null as NodeJS.Timeout|null,
      },
      state: {
        contrlShow: true,
        vol: 0.5,
        currentTime: 0,
        fullScreen: false,
        playing: false,
      },
      reaction: {
        showOptions: false,
        options: ['😂', '🤣', '😍'],
        active: {
          'NHI': false,
          'NLI': false,
          'PLI': false,
          'PHI': false,
        } as { [key: string]: boolean }
      },
      reactionStyle: {
        right: '0px',
        left: '0px',
        top: '0px',
        bottom: '0px',
        opacity: '0',
        'pointer-events': 'none'
      },
      lastClick: 0
    };
  },
  mounted() {
    this.init();
  },
  beforeDestroy() {
    document.body.removeEventListener("mousemove", this.mouseMoveAction);
    document.body.removeEventListener("mouseup", this.mouseUpAction);
  },
  methods: {
    init() {
      this.$video = this.$el.getElementsByTagName("video")[0];
      this.initCore();

      if (this.options.autoplay) {
        this.play();
      }

      document.body.addEventListener("mousemove", this.mouseMoveAction, false);
      document.body.addEventListener("mouseup", this.mouseUpAction, false);
    },
    initCore() {
      this.initVol();
      this.initVideo();
      this.initPlayer();

      const vol = this.options.volume || 0.9;
      this.setVol(vol);
    },
    initPlayer() {
      const $player = this.$el.getElementsByClassName('video-container')[0];
      this.player.$player = $player;
    },
    initVol() {
      const $volBox = this.$el.getElementsByClassName('video-volume-slider')[0];
    
      this.volume.$volBox = $volBox;
    
      this.volume.pos.start = $volBox.getBoundingClientRect().left;
      this.volume.pos.width = $volBox.getBoundingClientRect().width - this.volume.pos.innerWidth;
    },
    initVideo() {
    },
    mouseEnterVideo() {
      if (this.tmp.contrlHideTimer) {
        clearTimeout(this.tmp.contrlHideTimer);
        this.tmp.contrlHideTimer = null;
      }

      this.state.contrlShow = true;
    },
    mouseLeaveVideo() {
      if (this.tmp.contrlHideTimer) {
        clearTimeout(this.tmp.contrlHideTimer);
      }

      this.tmp.contrlHideTimer = setTimeout(() => {
        this.state.contrlShow = false;
        this.reaction.showOptions = false;
        this.tmp.contrlHideTimer = null;
        this.reactionStyle.opacity = '0';
        this.reactionStyle['pointer-events'] = 'none';

        const keys = Object.keys(this.reaction.active);
        for (const key of keys) {
          this.reaction.active[key] = false;
        }
      }, 2000);
    },
    toggleContrlShow() {
      this.state.contrlShow = !this.state.contrlShow;
    },
    getTime() {
      if (!this.$video) return;

      this.$video.addEventListener("progress", () => {
        if (!this.$video) return;

        this.video.loaded = (-1 + this.$video.buffered.end(0) / this.$video.duration) * 100;
      });

      this.video.len = this.$video.duration;
    },
    setVideoByTime(percent: number) {
      this.video.pos.current = percent * 100;
      const video = this.$refs.video as HTMLVideoElement;

      video.currentTime = video.duration * percent;
    },
    screenClick() {
      const newTime = new Date().getTime();
      if ((newTime - this.lastClick) < 200) {
        this.fullScreen();
      }

      this.lastClick = newTime;
      this.play();
    },
    play() {
      this.state.playing = !this.state.playing;
      if (this.$video) {
        if (this.state.playing) {
          this.$video.play();

          this.$video.addEventListener("timeupdate", this.timeline);
          this.$video.addEventListener("ended", () => {
            this.state.playing = false;
          });
        } else {
          this.$video.pause();
        }
      }
    },
    timeline() {
      if (!this.$video) return;
      const video = (this.$refs.video as HTMLVideoElement)

      this.video.pos.current = (video.currentTime / video.duration) * 100;

      this.video.displayTime = timeParse(
        this.$video.duration - this.$video.currentTime
      );

      const newTime = `00:${timeParse(this.$video.currentTime)}`;
      if (newTime !== this.lastTime) {
        this.$emit('progress', newTime);
        this.lastTime = newTime;
      }
    },
    volMove() {
      this.initVol();
      this.volume.moving = true;
    },
    videoMove() {
      this.initVideo();
      this.video.moving = true;
    },
    slideClick(e: MouseEvent) {
      this.videoSlideMove(e);
    },
    volSlideClick(e: MouseEvent) {
      this.volSlideMove(e);
    },
    volMuted() {
      if (!this.$video) return;
      this.$video.muted = !this.$video.muted;
      this.volume.muted = this.$video.muted;
    },
    setVol(val: number) {
      if (this.$video) {
        this.volume.pos.current = this.volume.pos.width - (val * this.volume.pos.width);
        this.volume.percent = val * 100;
        this.$video.volume = val;
      }
    },
    fullScreen() {
      this.state.fullScreen = (window.innerWidth == screen.width && window.innerHeight == screen.height);
      if (!this.state.fullScreen) {
        if (!this.$video) return;

        this.state.fullScreen = true;
        (this.$refs.videoContainer as HTMLElement).requestFullscreen();
      } else {
        this.state.fullScreen = false;
        document.exitFullscreen();
      }
      setTimeout(this.initVideo, 200);
    },
    mouseMoveAction(e: MouseEvent) {
      const rect = (this.$refs.video as HTMLVideoElement).getBoundingClientRect();
      if (e.clientY > rect.top && e.clientY < rect.bottom) {
        if (e.clientX > rect.left && e.clientX < rect.right) {
          this.state.contrlShow = true;
          this.mouseLeaveVideo();
        }
      }
    },
    contrlHider(e: MouseEvent) {
      const x = getMousePosition(e, "x");
      const y = getMousePosition(e, "y");

      if (!this.player.pos) {
        this.player.pos = (this.$refs.video as HTMLElement).getBoundingClientRect();
      }

      if (y > this.player.pos.top && y < this.player.pos.top + this.player.pos.height) {
        if (x > this.player.pos.left && x < this.player.pos.left + this.player.pos.width) {
          return this.mouseEnterVideo();
        }
      }

      return this.mouseLeaveVideo();
    },
    volSlideMove(e: MouseEvent) {
      const x = getMousePosition(e) - this.volume.pos.start;
      if (x > 0 && x < this.volume.pos.width) {
        this.setVol(x / this.volume.pos.width);
      }
    },
    videoSlideMove(e: MouseEvent) {
      // const x = getMousePosition(e) - this.video.pos.start;
      let target = e.target as HTMLElement;
      if (target.classList.contains('video-progress-rail-inner')) {
        target = target.parentElement as HTMLElement;
      }

      const rect = target.getBoundingClientRect();
      const x = e.clientX - rect.left;

      this.setVideoByTime(x / rect.width);

      // if (x > 0 && x < this.video.pos.width) {
      //   this.video.pos.current = x;
      //   this.setVideoByTime(x / this.video.pos.width);
      // }
    },
    mouseUpAction() {
      this.volume.moving = false;
      this.video.moving = false;
    },
    toggleReaction(e: MouseEvent) {
      this.reaction.showOptions = !this.reaction.showOptions;
      if (!this.reaction.showOptions) {
        this.reactionStyle.opacity = '0';
        this.reactionStyle['pointer-events'] = 'none';

        const keys = Object.keys(this.reaction.active);
        for (const key of keys) {
          this.reaction.active[key] = false;
        }
      }
    },
    reactionOptionHover(e: MouseEvent, category: string) {
      if (!e.target) return;
      const target = e.target as HTMLElement;

      if (!target.parentElement) return;

      this.reaction.options = this.category[category];
      const keys = Object.keys(this.reaction.active);
      for (const key of keys) {
        this.reaction.active[key] = (key === category);
      }

      const rect = target.getBoundingClientRect();
      const parentRect = target.parentElement.getBoundingClientRect();

      this.reactionStyle.right = `${rect.right}px`;
      if (this.reaction.options.length < 2) {
        this.reactionStyle.left = `${rect.left}px`;
      } else {
        this.reactionStyle.left = `${rect.left - rect.width}px`;
      }

      this.reactionStyle.top = `calc(${parentRect.top - rect.width}px - 0.5em)`;
      this.reactionStyle.bottom = `${parentRect.bottom}px`;

      this.reactionStyle.opacity = '100';
      this.reactionStyle['pointer-events'] = 'auto';
    },
    reactionMouseEnter() {
      if (this.tmp.reactionHideTimer) {
        clearTimeout(this.tmp.reactionHideTimer);
        this.tmp.reactionHideTimer = null;
      }
    },
    reactionMouseLeave() {
      if (this.tmp.reactionHideTimer) {
        clearTimeout(this.tmp.reactionHideTimer);
        this.tmp.reactionHideTimer = null;
      }

      this.tmp.reactionHideTimer = setTimeout(() => {
        this.reactionStyle.opacity = '0';
        this.reactionStyle['pointer-events'] = 'none';

        const keys = Object.keys(this.reaction.active);
        for (const key of keys) {
          this.reaction.active[key] = false;
        }

        this.reaction.showOptions = false;
      }, 2000);
    },
    selectedReaction(emoji: any) {
      if (this.$video) {
        this.selectedEmoji = emoji;
        this.state.playing = false;
        this.$video.pause();

        this.showModal = true;
      }
    },
    dismissModal() {
      this.reactionText = '';
      this.showModal = false;
    },
    async submitReaction() {
      if (this.$video) {
        try {
          await Api.newReaction(this.$axios, this.videoId, this.selectedEmoji.id, this.reactionText, `00:${timeParse(this.$video.currentTime)}`);
          this.showModal = false;
        } catch (e) {
          console.log(e.response.data);
        } 
      }
    }
  },
});
</script>

<style class="scss">
.video-reaction-modal-backdrop {
  background: rgba(0, 0, 0, 0.3);
  z-index: 9998;

  @apply absolute w-full h-full;
}

.video-reaction-modal-header {
  @apply text-lg;
}

.video-reaction-modal-text {
  @apply outline-none resize-none border-2 border-gray-300 p-2 block mb-2;
}

.video-reaction-modal {
  z-index: 9999;

  @apply p-2 rounded-md absolute bg-white;
}

.video-reaction-specific {
  transition: opacity 0.2s;

  @apply fixed flex flex-row pointer-events-auto;
}

.video-reaction-specific-option {
  transition: all 0.3s;
  filter: grayscale(100%);

  @apply text-3xl cursor-pointer h-10;
}

.video-reaction-specific-option:hover {
  filter: grayscale(0%);
}

.video-reaction-bar {
  transition: all 0.3s;

  @apply flex absolute bottom-8 w-full pointer-events-none items-center;
}

.video-reaction-col {
  @apply flex flex-row items-stretch;
}

.video-reaction-options {
  transition: all 0.3s;
  transform: translate3d(5rem, 0, 0);

  @apply flex flex-col select-none opacity-0 pointer-events-none ml-auto bg-gray-400 bg-opacity-25 p-1 rounded-md border-gray-50 border-solid border-opacity-25 border-2;
}

.video-reaction-option {
  transition: all 0.3s;
  filter: grayscale(100%);

  @apply text-3xl cursor-pointer;
}

.video-reaction-option-active {
  filter: grayscale(0%);
}

.video-reaction-option:hover {
  filter: grayscale(0%);
}

.video-reaction-bar-hidden {
  transform: translate3d(0, 1.3rem, 0);
}

.video-reaction-options-visible {
  transform: translate3d(0, 0, 0);

  @apply opacity-100 pointer-events-auto;
}

.video-reaction-bar-hidden .video-reaction-options {
  @apply opacity-0 pointer-events-none;
}

.video-reaction-btn {
  transition: all 0.3s;
  filter: grayscale(100%);

  @apply text-gray-500 cursor-pointer text-5xl p-3 select-none pointer-events-auto;
}

.video-reaction-btn:hover {
  filter: grayscale(0%);
  transform: scale(1.2);
}

.video-container {
  width: 100%;
  padding-top: 56.25%;
  position: relative;
  background-color: #000;
}

.video-container:fullscreen {
  padding-top: 0;
}

.video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  vertical-align: bottom;
}

.video-container:fullscreen > .video {
  position: relative;
}

.video-content {
  position: absolute;
  display: flex;
  left: 0;
  bottom: 0;
  height: 2rem;
  width: 100%;
  z-index: 2147483646;
  background: rgba(0, 0, 0, 0.281);
}

.video-play-btn {
  position: relative;
  background: none;
  border: none;
  height: 2rem;
  width: 4rem;
  outline: none;
  vertical-align: top;
  transition: transform 0.3s;
}

.video-play-btn:focus {
  outline: none;
}

.video-play-btn:hover {
  transform: scale(1.2);
}

.video-play-btn-icon {
  position: absolute;
  height: 1rem;
  width: 1rem;
  top: 50%;
  left: 50%;
  margin-top: -0.5rem;
  margin-left: -0.5rem;
}

.video-control-volume-btn-icon {
  position: absolute;
  height: 1.1rem;
  width: 1.1rem;
  top: 50%;
  left: 50%;
  margin-top: -0.55rem;
  margin-left: -0.55rem;
}

.video-volume-slider {
  position: relative;
  display: inline-block;
  width: 6rem;
  height: 2rem;
  overflow: hidden;
  transition: all 0.2s ease-in;
}

.video-volume-rail {
  cursor: pointer;
  position: absolute;
  top: 50%;
  width: 6rem;
  height: 0.2rem;
  margin-top: -0.05rem;
  background: #fff;
}

.video-volume-rail:hover {
  height: 0.3rem;
  top: calc(50% - 0.1rem);
}

.video-volume-rail-inner {
  @apply bg-green-400;

  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 0.2rem;
  transition: transform 0.2s;
}

.video-volume-rail:hover .video-volume-rail-inner {
  height: 0.3em;
}

.__cov-contrl-vol-inner {
  position: absolute;
  display: inline-block;
  left: 0;
  top: 50%;
  background: #fff;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  margin-top: -0.25rem;
  z-index: 2;
  cursor: pointer;
}

.video-control-volume-box {
  display: flex;
}

.video-progress-bar {
  position: relative;
  display: inline-block;
  height: 100%;
  width: 100%;
  overflow: hidden;
  margin: 0 0.5rem;
  transition: all 0.2s ease-in;
}

.video-progress-rail {
  cursor: pointer;
  position: absolute;
  top: 50%;
  width: 100%;
  height: 0.2rem;
  margin-top: -0.05rem;
  background: rgba(255, 255, 255, 0.5);
  overflow: hidden;
}

.video-progress-rail:hover {
  height: 0.3rem;
  top: calc(50% - 0.1rem);
}

.video-progress-rail-inner {
  @apply bg-green-400;

  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 0.2rem;
  transition: transform 0.2s;
}

.video-progress-rail:hover .video-progress-rail-inner {
  height: 0.3em;
}

.video-progress-inner {
  position: absolute;
  display: inline-block;
  left: 0;
  top: 50%;
  background: #fff;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  margin-top: -0.25rem;
  z-index: 2;
  cursor: pointer;
  transition: all 16ms;
}

.video-control-time {
  padding: 0 1rem;
}

.video-control-time-text {
  color: #fff;
  line-height: 2rem;
  font-size: 0.8rem;
}

::-webkit-media-controls {
  display: none !important;
}

video::-webkit-media-controls {
  display: none !important;
}

video::-webkit-media-controls-enclosure {
  display: none !important;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

@media all and (max-width: 768px) {
  .video-volume-slider {
    width: 3rem;
  }

  .video-control-time {
    padding: 0 0.2rem;
  }

  .video-control-volume-box .video-play-btn {
    width: 2rem;
  }
}
</style>
