let windowsize;
console.log(auth);
function reportWindowSize() {
  console.log(window.innerWidth + " - " + window.innerHeight);
  windowsize = window.innerWidth + " - " + window.innerHeight;
}

window.addEventListener('resize', reportWindowSize);