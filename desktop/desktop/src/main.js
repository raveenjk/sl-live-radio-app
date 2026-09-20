const { app, BrowserWindow, Menu, Tray, globalShortcut, nativeImage } = require('electron');
const path = require('path');

let mainWindow;
let tray = null;
let isQuitting = false;

// ── Single-instance lock ────────────────────────────────────────────
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      if (!mainWindow.isVisible()) mainWindow.show();
      mainWindow.focus();
    }
  });

  app.whenReady().then(() => {
    createWindow();
    createTray();
    registerGlobalShortcuts();
  });
}

// ── Window ──────────────────────────────────────────────────────────
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 900,
    height: 600,
    minWidth: 480,
    minHeight: 400,
    titleBarStyle: 'hidden',
    titleBarOverlay: {
      color: '#0f0f1a',
      symbolColor: '#ffffff',
      height: 32
    },
    title: 'SL Live Radio',
    icon: getTrayIcon(),
    backgroundColor: '#0f0f1a',
    show: false, // Don't show until ready
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false
    }
  });

  // Show window only when page is ready (avoids white flash)
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Load the web app
  mainWindow.loadURL('https://sl-live-radio-app.vercel.app/');

  // Hide on close instead of quitting (keep radio playing in background)
  mainWindow.on('close', (event) => {
    if (!isQuitting) {
      event.preventDefault();
      mainWindow.hide();
    }
  });

  // Cleanup reference
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// ── Tray Icon Helper ────────────────────────────────────────────────
function getTrayIcon() {
  // Try loading custom icon first
  const iconPath = path.join(__dirname, '..', 'build', 'icon.png');
  try {
    const icon = nativeImage.createFromPath(iconPath);
    if (!icon.isEmpty()) return icon.resize({ width: 16, height: 16 });
  } catch (e) {
    // Fall through to generated icon
  }

  // Fallback: generate a simple 16x16 icon programmatically
  // This is a 16x16 PNG with a blue circle (radio icon placeholder)
  const size = 16;
  const canvas = Buffer.alloc(size * size * 4); // RGBA
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const idx = (y * size + x) * 4;
      const cx = x - 7.5, cy = y - 7.5;
      const dist = Math.sqrt(cx * cx + cy * cy);
      if (dist <= 7) {
        canvas[idx] = 0x4a;     // R
        canvas[idx + 1] = 0x9e; // G
        canvas[idx + 2] = 0xff; // B
        canvas[idx + 3] = 0xff; // A
      } else {
        canvas[idx + 3] = 0x00; // Transparent
      }
    }
  }
  return nativeImage.createFromBuffer(canvas, { width: size, height: size });
}

// ── System Tray ─────────────────────────────────────────────────────
function createTray() {
  const icon = getTrayIcon();
  tray = new Tray(icon);

  const contextMenu = Menu.buildFromTemplate([
    {
      label: 'Show SL Live Radio',
      click: () => {
        if (mainWindow) {
          mainWindow.show();
          mainWindow.focus();
        }
      }
    },
    {
      label: 'Play / Pause',
      click: () => {
        if (mainWindow) mainWindow.webContents.send('media-play-pause');
      }
    },
    { type: 'separator' },
    {
      label: 'Quit',
      click: () => {
        isQuitting = true;
        app.quit();
      }
    }
  ]);

  tray.setToolTip('SL Live Radio');
  tray.setContextMenu(contextMenu);

  // Single click on tray icon = show the window
  tray.on('click', () => {
    if (mainWindow) {
      mainWindow.show();
      mainWindow.focus();
    }
  });
}

// ── Global Media Shortcuts ──────────────────────────────────────────
function registerGlobalShortcuts() {
  const shortcuts = {
    'MediaPlayPause': 'media-play-pause',
    'MediaNextTrack': 'media-next-track',
    'MediaPreviousTrack': 'media-previous-track'
  };

  for (const [key, channel] of Object.entries(shortcuts)) {
    try {
      globalShortcut.register(key, () => {
        if (mainWindow) mainWindow.webContents.send(channel);
      });
    } catch (e) {
      console.warn(`Could not register shortcut ${key}:`, e.message);
    }
  }
}

// ── Cleanup ─────────────────────────────────────────────────────────
app.on('before-quit', () => {
  isQuitting = true;
});

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});

app.on('window-all-closed', () => {
  // On Windows, don't quit when all windows are closed (tray keeps running)
});
