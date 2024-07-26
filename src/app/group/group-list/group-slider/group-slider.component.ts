// // import { Component, Input } from '@angular/core';
// // import { Group } from '../../group.model';
// // @Component({
// //   selector: 'app-group-slider',
// //   templateUrl: './group-slider.component.html',
// //   styleUrls: ['./group-slider.component.css']
// // })
// // export class GroupSliderComponent {
// //   @Input() groups: Group[] = [];
// //   currentIndex: number = 0;

// //   nextSlide() {
// //     if (this.currentIndex < this.groups.length - 5) {
// //       this.currentIndex++;
// //     }
// //   }

// //   prevSlide() {
// //     if (this.currentIndex > 0) {
// //       this.currentIndex--;
// //     }
// //   }
// // }

// import { Component, Input } from '@angular/core';
// // import { Group } from '../../group.model';
// interface Group {
//   id: number;
//   name: string;
//   description: string;
// }

// @Component({
//   selector: 'app-group-slider',
//   templateUrl: './group-slider.component.html',
//   styleUrls: ['./group-slider.component.css']
// })
// export class GroupSliderComponent {
//   @Input() groups: Group[] = [];
//   currentIndex: number = 0;

//   // Number of items visible in the slider
//   itemsVisible: number = 5;

//   nextSlide() {
//     if (this.currentIndex < this.groups.length - this.itemsVisible) {
//       this.currentIndex++;
//       console.log('Next Slide:', this.currentIndex);
//     } else {
//       console.log('At the end of the slider');
//     }
//   }

//   prevSlide() {
//     if (this.currentIndex > 0) {
//       this.currentIndex--;
//       console.log('Previous Slide:', this.currentIndex);
//     } else {
//       console.log('At the beginning of the slider');
//     }
//   }
// }

import { Component, Input } from '@angular/core';
import { Group } from '../../group.model';
interface Groupi {
  id: number;
  name: string;
  description: string;
}

@Component({
  selector: 'app-group-slider',
  templateUrl: './group-slider.component.html',
  styleUrls: ['./group-slider.component.css']
})
export class GroupSliderComponent {
  @Input() groups: Group[] = [];
  currentIndex: number = 0;

  // Number of items visible in the slider
  itemsVisible: number = 5;

  nextSlide() {
    if (this.currentIndex < this.groups.length - this.itemsVisible) {
      this.currentIndex++;
      console.log('Next Slide:', this.currentIndex);
    } else {
      console.log('At the end of the slider');
    }
  }

  prevSlide() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      console.log('Previous Slide:', this.currentIndex);
    } else {
      console.log('At the beginning of the slider');
    }
  }
}
