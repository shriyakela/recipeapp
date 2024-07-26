// import { Component } from '@angular/core';
// import { ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
// import { GroupService } from '../group.service';
// @Component({
//   selector: 'app-group-start',
//   templateUrl: './group-start.component.html',
//   styleUrl: './group-start.component.css'
// })
// export class GroupStartComponent {
//   groupForm: FormGroup;

//   constructor(
//     private fb: FormBuilder,
//     private groupService: GroupService
//   ) {
//     this.groupForm = this.fb.group({
//       name: ['', [Validators.required, Validators.minLength(2)]],
//       description: ['']
//     });
//   }

//   onSubmit() {
//     if (this.groupForm.valid) {
//       const groupData = this.groupForm.value;
//       this.groupService.createGroup(groupData).subscribe(
//         response => {
//           console.log('Group created successfully:', response);
//           // Handle success response, show success message, etc.
//         }
//       );
//     }
//   }
// }
import { Component } from '@angular/core';
import { ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { GroupService } from '../group.service';

@Component({
  selector: 'app-group-start',
  templateUrl: './group-start.component.html',
  styleUrls: ['./group-start.component.css']
})
export class GroupStartComponent {
  groupForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private groupService: GroupService
  ) {
    this.groupForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      description: [''],
      isPublic: [false]  // Initialize the isPublic control with a default value of false
    });
  }

  onSubmit() {
    if (this.groupForm.valid) {
      const groupData = this.groupForm.value;
      this.groupService.createGroup(groupData).subscribe(
        {next: response => {
          console.log('Group created successfully:', response);
          // Handle success response, show success message, etc.
        },
        error: error => {
          console.error('Error creating group:', error);
          // Handle error response, show error message, etc.
        }}
      );
    }
  }
  // onSubmit() {
  //   if (this.groupForm.valid) {
  //     const groupData = this.groupForm.value;
  //     this.groupService.createGroup(groupData).subscribe({
  //       next: (response) => {
  //         console.log('Group created successfully:', response);
  //         // Handle success (e.g., show a success message, navigate to the new group)
  //       },
  //       error: (error) => {
  //         console.error('Error creating group:', error);
  //         if (error.error && error.error.msg) {
  //           // Display the error message from the server
  //           console.error('Server error:', error.error.msg);
  //         } else {
  //           // Display a generic error message
  //           console.error('An unexpected error occurred');
  //         }
  //         // Handle error (e.g., show an error message to the user)
  //       }
  //     });
  //   }
  // }
}
