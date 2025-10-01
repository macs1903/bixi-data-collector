name: Debug PAT Push

on:
  workflow_dispatch:   # Lancer manuellement pour tester

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Check if PAT is loaded
        env:
          GH_PAT: ${{ secrets.GH_PAT }}
        run: |
          if [ -z "$GH_PAT" ]; then
            echo "❌ GH_PAT is empty!"
            exit 1
          else
            echo "✅ GH_PAT loaded, length: ${#GH_PAT}"
          fi

      - name: Create dummy file
        run: echo "Run at $(date)" > test.txt

      - name: Commit and push
        env:
          GH_PAT: ${{ secrets.GH_PAT }}
        run: |
          git config --global user.name "github-actions"
          git config --global user.email "actions@github.com"
          git remote set-url origin https://x-access-token:${GH_PAT}@github.com/macs1903/bixi-data-collector.git
          git add test.txt
          git commit -m "Test commit [skip ci]" || echo "No changes"
          git push origin HEAD:main
