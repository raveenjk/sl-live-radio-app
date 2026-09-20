import webview
import ctypes
import os

# Optimize WebView2 performance (reduces lag on some Intel/AMD GPUs)
os.environ["WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS"] = "--enable-gpu-rasterization --ignore-gpu-blocklist"

try:
    user32 = ctypes.windll.user32
    GWL_STYLE = -16
    WS_CAPTION = 0x00C00000
    WS_THICKFRAME = 0x00040000
    WS_SYSMENU = 0x00080000
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001
    SWP_NOZORDER = 0x0004
    SWP_FRAMECHANGED = 0x0020
except:
    pass

class Api:
    def __init__(self):
        self.window = None
        self.is_mini = False
        self.normal_width = 900
        self.normal_height = 600

    def toggle_frame(self, hide):
        try:
            hwnd = user32.FindWindowW(None, 'SL Live Radio')
            if not hwnd: return
            style = user32.GetWindowLongW(hwnd, GWL_STYLE)
            if hide:
                style &= ~(WS_CAPTION | WS_THICKFRAME | WS_SYSMENU)
            else:
                style |= (WS_CAPTION | WS_THICKFRAME | WS_SYSMENU)
            user32.SetWindowLongW(hwnd, GWL_STYLE, style)
            user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
        except Exception as e:
            pass

    def toggle_mini(self):
        self.is_mini = not self.is_mini
        if self.is_mini:
            self.toggle_frame(hide=True)
            self.window.evaluate_js("document.body.classList.add('mini-mode');")
            self.window.resize(450, 240)
            self.window.on_top = True
        else:
            self.window.evaluate_js("document.body.classList.remove('mini-mode');")
            self.toggle_frame(hide=False)
            self.window.resize(self.normal_width, self.normal_height)
            self.window.on_top = False

def inject_ui(window):
    css = """
    /* Hide the real app in mini mode securely */
    body.mini-mode > :not(#custom-mini-player) {
        display: none !important;
    }
    body.mini-mode {
        background: transparent !important;
        overflow: hidden !important;
    }
    
    /* Toggle Button - Optimized (Removed backdrop-filter which causes lag) */
    .btn-to-mini {
        position: fixed;
        top: 20px;
        right: 150px;
        z-index: 9999;
        background: rgba(20, 20, 20, 0.8);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        transition: background 0.2s;
    }
    .btn-to-mini:hover { background: rgba(50, 50, 50, 0.9); }
    body.mini-mode .btn-to-mini { display: none !important; }

    /* Custom Mini Player Design - Optimized shadows */
    #custom-mini-player {
        display: none;
    }
    body.mini-mode #custom-mini-player {
        display: flex;
        flex-direction: column;
        width: 100vw;
        height: 100vh;
        background: linear-gradient(180deg, #222b36 0%, #171d24 100%);
        color: #fff;
        font-family: 'Segoe UI', system-ui, sans-serif;
        box-sizing: border-box;
        padding: 16px 20px;
        -webkit-app-region: drag;
        border: 1px solid #323d4a;
        border-radius: 12px;
    }
    
    /* Header */
    .cmp-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
    }
    .cmp-logo {
        display: flex;
        align-items: center;
        gap: 6px;
        font-weight: 800;
        font-size: 15px;
        color: #fff;
    }
    .cmp-logo svg { fill: #f98b26; width: 16px; height: 16px; }
    .cmp-dot {
        width: 6px;
        height: 6px;
        background: #f98b26;
        border-radius: 50%;
        margin-left: 6px;
    }
    .cmp-controls-top {
        display: flex;
        gap: 8px;
        -webkit-app-region: no-drag;
    }
    .cmp-btn {
        background: #252e38;
        border: 1px solid #323d4a;
        color: #8c97a5;
        border-radius: 8px;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 16px;
        padding: 0;
    }
    .cmp-btn:hover { background: #323d4a; color: #fff; }

    /* Body */
    .cmp-body {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .cmp-art {
        width: 80px;
        height: 80px;
        border-radius: 16px;
        background-color: #333;
        background-size: cover;
        background-position: center;
        border: 2px solid #f98b26;
    }
    .cmp-info { flex: 1; overflow: hidden; }
    .cmp-status {
        color: #f98b26;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .cmp-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 4px;
        margin-top: 0;
        white-space: nowrap;
        text-overflow: ellipsis;
        overflow: hidden;
    }
    .cmp-subtitle {
        font-size: 13px;
        color: #8c97a5;
        white-space: nowrap;
    }

    /* Playback controls */
    .cmp-playback {
        display: flex;
        align-items: center;
        gap: 12px;
        -webkit-app-region: no-drag;
    }
    .cmp-play-btn {
        width: 52px;
        height: 52px;
        border-radius: 50%;
        border: 2px solid #f98b26;
        background: transparent;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    .cmp-play-btn svg { width: 24px; height: 24px; fill: currentColor; }
    
    .cmp-skip-btn {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 1px solid #323d4a;
        background: transparent;
        color: #8c97a5;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    .cmp-skip-btn svg { width: 18px; height: 18px; fill: currentColor; }

    /* Footer */
    .cmp-footer {
        margin-top: auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        -webkit-app-region: no-drag;
    }
    .cmp-volume {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #202832;
        padding: 6px 14px;
        border-radius: 12px;
        border: 1px solid #2a3441;
    }
    .cmp-volume span { font-size: 14px; color: #8c97a5; }
    .cmp-volume input[type=range] {
        -webkit-appearance: none;
        width: 100px;
        height: 4px;
        background: #f98b26;
        border-radius: 2px;
    }
    .cmp-volume input[type=range]::-webkit-slider-thumb {
        -webkit-appearance: none;
        width: 12px;
        height: 12px;
        background: #f98b26;
        border-radius: 50%;
        cursor: pointer;
    }
    .cmp-hint {
        font-size: 11px;
        color: #5d6875;
    }
    """
    window.load_css(css)
    
    js = """
    // Add normal toggle button
    const btn = document.createElement('button');
    btn.className = 'btn-to-mini';
    btn.innerHTML = '⛶ Mini Player';
    btn.onclick = () => { if (window.pywebview) pywebview.api.toggle_mini(); };
    document.body.appendChild(btn);

    // Inject Custom Mini Player
    const cmp = document.createElement('div');
    cmp.id = 'custom-mini-player';
    cmp.innerHTML = `
      <div class="cmp-header">
        <div class="cmp-logo">
          <svg viewBox="0 0 24 24"><rect x="2" y="6" width="4" height="12"/><rect x="10" y="2" width="4" height="20"/><rect x="18" y="8" width="4" height="8"/></svg>
          IslandRadio.lk
          <span class="cmp-dot"></span>
        </div>
        <div class="cmp-controls-top">
          <button class="cmp-btn" id="cmp-restore" title="Restore">↗</button>
        </div>
      </div>
      
      <div class="cmp-body">
        <div class="cmp-art" id="cmp-art"></div>
        <div class="cmp-info">
          <div class="cmp-status" id="cmp-status">READY TO PLAY</div>
          <div class="cmp-title" id="cmp-title">Select a station</div>
          <div class="cmp-subtitle" id="cmp-subtitle">--</div>
        </div>
        <div class="cmp-playback">
          <button class="cmp-skip-btn" id="cmp-prev">
            <svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg>
          </button>
          <button class="cmp-play-btn" id="cmp-play">
             <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
          </button>
          <button class="cmp-skip-btn" id="cmp-next">
            <svg viewBox="0 0 24 24"><path d="M9 18l6-6-6-6"/></svg>
          </button>
        </div>
      </div>
      
      <div class="cmp-footer">
        <div class="cmp-volume">
          <span>🔊</span>
          <input type="range" id="cmp-vol" min="0" max="1" step="0.01">
          <span id="cmp-vol-text">100%</span>
        </div>
        <div class="cmp-hint">Double-click tray icon for full player</div>
      </div>
    `;
    document.body.appendChild(cmp);

    // Logic to tie CMP to Real Player
    document.getElementById('cmp-restore').onclick = () => { if(window.pywebview) pywebview.api.toggle_mini(); };
    
    document.getElementById('cmp-prev').onclick = () => {
        const b = document.querySelector('#btnCarouselPrev, .carousel__arrow--prev');
        if(b) b.click();
    };
    document.getElementById('cmp-next').onclick = () => {
        const b = document.querySelector('#btnCarouselNext, .carousel__arrow--next');
        if(b) b.click();
    };
    document.getElementById('cmp-play').onclick = () => {
        const b = document.querySelector('#btnPlay, #popPlay, .ctrl--play');
        if(b) b.click();
    };
    
    const volInput = document.getElementById('cmp-vol');
    const volText = document.getElementById('cmp-vol-text');
    volInput.oninput = (e) => {
        const realVol = document.getElementById('volumeSlider') || document.getElementById('popVolume');
        if(realVol) {
            realVol.value = e.target.value;
            realVol.dispatchEvent(new Event('input', {bubbles:true}));
            realVol.dispatchEvent(new Event('change', {bubbles:true}));
        }
        volText.innerText = Math.round(e.target.value * 100) + '%';
    };

    // Cache DOM lookups for performance
    const cmpTitle = document.getElementById('cmp-title');
    const cmpStatus = document.getElementById('cmp-status');
    const cmpSubtitle = document.getElementById('cmp-subtitle');
    const cmpPlay = document.getElementById('cmp-play');
    const cmpArt = document.getElementById('cmp-art');

    // Run interval less frequently and optimized
    setInterval(() => {
        if (!document.body.classList.contains('mini-mode')) return; // Skip work if not in mini-mode
        
        const nameEl = document.getElementById('playerName') || document.getElementById('popName');
        if(nameEl && cmpTitle.innerText !== nameEl.innerText) cmpTitle.innerText = nameEl.innerText;
        
        const statusEl = document.getElementById('playerStatus') || document.querySelector('.pop__status');
        if(statusEl && cmpStatus.innerText !== statusEl.innerText) cmpStatus.innerText = statusEl.innerText;
        
        const langEl = document.getElementById('playerLang');
        const freqEl = document.getElementById('playerFreq');
        let subtitle = '';
        if(langEl && langEl.innerText) subtitle += langEl.innerText;
        if(freqEl && freqEl.innerText) subtitle += (subtitle ? ' • ' : '') + freqEl.innerText;
        if(cmpSubtitle.innerText !== (subtitle || '--')) cmpSubtitle.innerText = subtitle || '--';

        const playBtn = document.getElementById('btnPlay') || document.getElementById('popPlay');
        const isPlaying = playBtn && playBtn.querySelector('.icon-pause') && playBtn.querySelector('.icon-pause').style.display !== 'none';
        
        // Only update DOM if state changed
        const currentPlayState = cmpPlay.dataset.playing === 'true';
        if (isPlaying !== currentPlayState) {
            cmpPlay.dataset.playing = isPlaying ? 'true' : 'false';
            cmpPlay.innerHTML = isPlaying 
                ? '<svg viewBox="0 0 24 24"><path d="M6 4h4v16H6zm8 0h4v16h-4z"/></svg>' 
                : '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>';
        }
            
        const logoEl = document.getElementById('mainLogo') || document.getElementById('popLogo');
        if(logoEl) {
            const img = logoEl.querySelector('img');
            if(img && img.src) {
                const url = `url(${img.src})`;
                if(cmpArt.style.backgroundImage !== url) {
                    cmpArt.style.backgroundImage = url;
                }
            }
        }
    }, 800);
    """
    window.evaluate_js(f"setTimeout(() => {{ {js} }}, 1000);")

def main():
    api = Api()
    window = webview.create_window(
        title='SL Live Radio',
        url='https://sl-live-radio-app.vercel.app/',
        width=900,
        height=600,
        min_size=(400, 120),
        js_api=api
    )
    api.window = window
    webview.start(inject_ui, window)

if __name__ == '__main__':
    main()
