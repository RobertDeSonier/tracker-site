# tracker-site

## Steps taken:

1. Set up MongoDB and created collections: `Users`, `Items`, and `Records`.
    - `net start MongoDB`
    - `mongosh`
    - `use tracker_site`
2. Created a Python virtual environment and installed necessary packages: `django`, `djongo`, `pytz`, `mongoengine`, and `werkzeug`.
    - `python -m venv c:\src\personal\tracker-site\backend\venv`
    - `.\backend\venv\Scripts\activate`
3. Created a Django app named `tracker_app`.
    - `python backend/tracker/manage.py startapp tracker_app`
4. Implemented user authentication APIs:
   - `register`: To register a new user.
   - `login`: To log in a user.
   - `logout`: To log out a user.
5. Added user profile management APIs:
   - `view_profile`: To view user profile details.
   - `update_profile`: To update user profile information.
6. Implemented item management APIs:
   - `list_items`: To list all items for a user.
   - `update_item`: To update an item's description.
   - `delete_item`: To delete an item.
7. Implemented record management APIs:
   - `list_records`: To list all records for an item.
   - `update_record`: To update a record's action, timestamp, or comment.
   - `delete_record`: To delete a record.
8. Updated the `Record` model and related APIs to include a `comment` field.

9. **Initialize React App**:
   - Created a React app using `create-react-app`.

10. **Folder Structure**:
   - Organized the frontend into `components`, `pages`, `services`, `styles`, and `utils` directories for better modularity.

11. **Routing**:
   - Set up React Router for navigation between pages like Home, Login, Register, Dashboard, and Profile.

12. **Axios Configuration**:
   - Configured Axios for making API calls to the backend.
   - Added interceptors for token-based authentication.

13. **Authentication**:
   - Implemented login and registration pages.
   - Integrated token-based authentication using JWT.
   - Stored tokens in `localStorage` and added token refresh functionality.

14. **Protected Routes**:
   - Created a `ProtectedRoute` component to restrict access to certain pages for authenticated users only.

15. **Styling**:
   - Added basic styling using CSS files for components and pages.
