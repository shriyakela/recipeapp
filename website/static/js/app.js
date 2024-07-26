function scrollGroups(direction) {
    const container = document.querySelector('.group-scroll');
    const scrollAmount = container.offsetWidth;
    container.scrollBy({
      left: direction * scrollAmount,
      behavior: 'smooth'
    });
  }