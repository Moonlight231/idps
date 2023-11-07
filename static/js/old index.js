const sideLinks = document.querySelectorAll('.sidebar .side-menu li a:not(.logout)');

sideLinks.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', () => {
        sideLinks.forEach(i => {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});

const sideBar = document.querySelector('.sidebar');

function toggleside() {
    if (sideBar.classList.contains('close')) {
      sideBar.classList.remove('close');
      localStorage.setItem("sideStatus", "expanded");
    } else {
      sideBar.classList.add('close');
      localStorage.setItem("sideStatus", "closed");
      
    }
  }
  
  if (localStorage.getItem("sideStatus") === "closed") {
    sideBar.classList.add('close');
  }

document.querySelector('.content nav .bx.bx-menu').addEventListener('click', toggleside);






const searchBtn = document.querySelector('.content nav form .form-input button');
const searchBtnIcon = document.querySelector('.content nav form .form-input button .bx');
const searchForm = document.querySelector('.content nav form');

searchBtn.addEventListener('click', function (e) {
    if (window.innerWidth < 576) {
        e.preventDefault;
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchBtnIcon.classList.replace('bx-search', 'bx-x');
        } else {
            searchBtnIcon.classList.replace('bx-x', 'bx-search');
        }
    }
});

window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        sideBar.classList.add('close');
    } else {
        sideBar.classList.remove('close');
    }
    if (window.innerWidth > 576) {
        searchBtnIcon.classList.replace('bx-x', 'bx-search');
        searchForm.classList.remove('show');
    }
});

const body = document.querySelector('body');
const darkMode = document.querySelector('.dark-mode');

function toggleDark() {
    if (body.classList.contains('dark-mode-variables')) {
      body.classList.remove('dark-mode-variables');
      darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
      darkMode.querySelector('span:nth-child(2)').classList.remove('active');
      
      localStorage.setItem("theme", "light");
    } else {
      body.classList.add('dark-mode-variables');
      darkMode.querySelector('span:nth-child(1)').classList.remove('active');
      darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
      localStorage.setItem("theme", "dark");
      
    }

  }
  
  if (localStorage.getItem("theme") === "dark") {
    darkMode.querySelector('span:nth-child(1)').classList.remove('active');
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
    body.classList.add('dark-mode-variables');
  }

document.querySelector('.dark-mode').addEventListener('click', toggleDark);




/*
const darkMode = document.querySelector('.dark-mode');

darkMode.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode-variables');
    darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
});

*/

//modal

function openModal() {
  document.querySelector('.modal-bg').style.display = 'flex';
}

function closeModal() {
  document.querySelector('.modal-bg').style.display = 'none';
}

document.querySelector('.report').addEventListener('click', function() {
  openModal();
});
