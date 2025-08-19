export interface JobApplication {
  id?: string; // Changed to string to support UUIDs
  jobId: string; // Changed from number to string to support UUIDs
  userId: number;
  applicationDate: string;
  status: 'Applied' | 'Under Review' | 'Interview' | 'Rejected' | 'Accepted' | 'Withdrawn';
  fullName?: string;
  email?: string;
  phone?: string;
  coverLetter?: string;
  resumePath?: string; // Store file path if uploaded
  quickApply?: boolean;
}

// Interface for sending application data to backend
export interface JobApplicationRequest {
  job_id: string;  // Backend expects job_id
  cover_letter?: string;  // Backend expects cover_letter
  resume_url?: string;  // Backend expects resume_url
}