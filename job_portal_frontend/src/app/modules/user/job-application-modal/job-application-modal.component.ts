import { Component, Input, Output, EventEmitter } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Job } from '../../../core/models/job.model';

@Component({
  selector: 'app-job-application-modal',
  standalone: true,
  imports: [FormsModule],
  template: `
    <div class="modal-backdrop" (click)="close()"></div>
    <div class="modal-content">
      <h2>Apply for Job</h2>
      <form (ngSubmit)="submitApplication()">
        <label for="coverLetter">Cover Letter</label>
        <textarea id="coverLetter" [(ngModel)]="coverLetter" name="coverLetter"></textarea>
        <button type="submit">Submit Application</button>
        <button type="button" (click)="close()">Cancel</button>
      </form>
    </div>
  `,
  styles: [`
    .modal-backdrop {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.5);
      z-index: 1000;
    }
    .modal-content {
      position: fixed;
      top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      background: #fff;
      padding: 2rem;
      border-radius: 8px;
      z-index: 1001;
      min-width: 300px;
    }
    textarea {
      width: 100%;
      min-height: 80px;
      margin-bottom: 1rem;
    }
    button {
      margin-right: 0.5rem;
    }
  `]
})
export class JobApplicationModalComponent {
  @Input() job: Job | null = null;
  @Output() closed = new EventEmitter<void>();
  @Output() applicationSubmitted = new EventEmitter<{ jobId: string | null, coverLetter: string }>();

  coverLetter = '';

  close() {
    this.closed.emit();
  }

  submitApplication() {
    if (this.job) {
      this.applicationSubmitted.emit({ jobId: this.job.id, coverLetter: this.coverLetter });
    }
    this.close();
  }
}
