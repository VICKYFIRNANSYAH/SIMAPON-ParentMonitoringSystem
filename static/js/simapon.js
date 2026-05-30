document.addEventListener("DOMContentLoaded", function () {
  // Simple DataTables initialization
  if (window.simpleDatatables) {
    document.querySelectorAll(".datatable").forEach((table) => {
      new simpleDatatables.DataTable(table, {
        searchable: true,
        fixedHeight: false,
        perPage: 10,
        labels: {
          placeholder: "Cari data...",
          perPage: "data per halaman",
          noRows: "Data belum tersedia",
          info: "Menampilkan {start} sampai {end} dari {rows} data",
        },
      });
    });
  }

  // Shrink Navbar on Scroll
  const navbar = document.querySelector(".app-navbar");
  if (navbar) {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        navbar.classList.add("scrolled");
      } else {
        navbar.classList.remove("scrolled");
      }
    };
    window.addEventListener("scroll", handleScroll);
    handleScroll(); // Run once in case already scrolled on mount
  }

  // Premium Loading Screen Fade Out
  const loadingScreen = document.getElementById("loading-screen");
  if (loadingScreen) {
    setTimeout(() => {
      loadingScreen.classList.add("opacity-0", "scale-105", "pointer-events-none");
      setTimeout(() => {
        loadingScreen.remove();
      }, 700); // Matches the transition duration (700ms)
    }, 1200); // 1.2s premium load delay
  }
});

// Original togglePassword function preserved exactly
function togglePassword(btn) {
  try {
    const container = btn.closest("td") || btn.parentElement;
    const mask = container.querySelector(".password-mask");
    if (!mask) return;

    if (mask.dataset.revealed === "1") {
      mask.textContent = "••••••••";
      mask.dataset.revealed = "0";
      btn.title = "Tampilkan/Sembunyikan Password";
      return;
    }

    mask.textContent = "Reset via Edit";
    mask.dataset.revealed = "1";
    btn.title = "Reset melalui halaman edit";
  } catch (error) {
    console.error(error);
  }
}

// Original togglePasswordInput function preserved exactly
function togglePasswordInput(inputId, iconId) {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(iconId);

  if (!input || !icon) return;

  if (input.type === "password") {
    input.type = "text";
    icon.innerHTML =
      '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path>';
    return;
  }

  input.type = "password";
  icon.innerHTML =
    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>';
}

// ==========================================================================
// Logika Interaktif Notifikasi & Toast
// ==========================================================================

// Floating Toasts Lifecycles
document.addEventListener("DOMContentLoaded", function () {
  const toasts = document.querySelectorAll(".toast-item");
  toasts.forEach((toast, index) => {
    // Staggered entrance animation
    setTimeout(() => {
      toast.classList.add("toast-slide-in");
    }, 150 + index * 180);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
      dismissToast(toast);
    }, 5500 + index * 180);
  });
});

function dismissToast(toast) {
  if (!toast) return;
  toast.classList.remove("toast-slide-in");
  toast.classList.add("toast-slide-out");
  
  // Clean up element after animation finishes
  setTimeout(() => {
    toast.remove();
  }, 400);
}
