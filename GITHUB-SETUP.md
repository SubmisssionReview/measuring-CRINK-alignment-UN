# Publishing to GitHub

This guide explains how to publish your local repository to GitHub.

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in to your account
2. Click the **"+"** icon in the top-right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `measuring-CRINK-alignment-UN`
   - **Description**: `Analysis of CRINK (China, Russia, Iran, North Korea) political alignment in UN voting patterns`
   - **Visibility**: Select **Public** (for academic sharing)
   - **Do NOT initialize** with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

## Step 2: Add Remote and Push

After creating the repository on GitHub, you'll see instructions. Run these commands in your terminal from the repository root:

```bash
# Navigate to your local repository
cd c:\Users\Lucian\measuring-CRINK-alignment-UN

# Add the remote repository
git remote add origin https://github.com/LBumeder/measuring-CRINK-alignment-UN.git

# Verify the remote was added
git remote -v

# Push your code to GitHub
git branch -M main
git push -u origin main
```

**Replace `LBumeder`** with your actual GitHub username.

## Step 3: Verify on GitHub

1. Go to your GitHub repository page
2. You should see all your files and folders
3. The README.md will be displayed automatically on the repository home page

## Step 4: (Optional) Enable GitHub Pages for Documentation

If you want to host documentation:

1. Go to repository **Settings** â†’ **Pages**
2. Select **Deploy from a branch**
3. Choose `main` branch and `/root` folder
4. Save

## Sharing Your Repository

Once published, you can share the repository link:

```
https://github.com/LBumeder/measuring-CRINK-alignment-UN
```

Share this URL with:
- Collaborators
- Journal reviewers
- Colleagues
- Data repositories (e.g., Harvard Dataverse can link to this)

## Next Steps

After pushing to GitHub:

1. Update the links in `README.md`:
   - Replace `LBumeder` with your GitHub username
   - Add Dataverse DOI when available

2. Add actual data files to `data/processed/` and configure `.gitignore`

3. Add your refactored notebooks to `notebooks/`

4. Create the documentation files in `docs/`

5. Tag a release when ready for publication:
   ```bash
   git tag -a v1.0.0 -m "Version 1.0.0 - Publication Release"
   git push origin v1.0.0
   ```

## Troubleshooting

### "Repository not found" error
- Verify the repository name matches exactly what you created on GitHub
- Check your username is correct
- Ensure you're using HTTPS URL (not SSH) unless you have SSH keys configured

### Permission denied
- If using HTTPS, GitHub may prompt for authentication
- Use a [Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) instead of your password
- If using SSH, ensure your SSH keys are set up properly

### Changes not showing
- Verify with `git remote -v`
- Try: `git push origin main --force` (only if necessary)

## Additional Resources

- [GitHub Docs: Create a Repo](https://docs.github.com/en/get-started/quickstart/create-a-repo)
- [GitHub Docs: Pushing Changes](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository)

