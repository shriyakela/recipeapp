import { Component } from '@angular/core';
import { ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { GroupService } from '../group.service';
@Component({
  selector: 'app-group-start',
  templateUrl: './group-start.component.html',
  styleUrl: './group-start.component.css'
})
export class GroupStartComponent {
  groupForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private groupService: GroupService
  ) {
    this.groupForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      description: ['']
    });
  }

  onSubmit() {
    if (this.groupForm.valid) {
      const groupData = this.groupForm.value;
      this.groupService.createGroup(groupData).subscribe(
        response => {
          console.log('Group created successfully:', response);
          // Handle success response, show success message, etc.
        }
      );
    }
  }
}
