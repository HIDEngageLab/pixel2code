      - name: Run initialize-command.sh
        run: |
          chmod +x ${{ github.workspace }}/meta-emblincram/toolbox/initialize-command.sh
          ${{ github.workspace }}/meta-emblincram/toolbox/initialize-command.sh ${{ github.workspace }}

      - name: Run Yocto Build
        run: |
          cd ..
          pwd
          ls
          docker run --rm \
            -v ${{ github.workspace }}:/workspace \
            ghcr.io/emblincram/devcon:latest /bin/bash -i -c "
              set -euo pipefail
              chmod +x ${{ github.workspace }}/meta-emblincram/toolbox/post-create-command.sh
              ${{ github.workspace }}/meta-emblincram/toolbox/post-create-command.sh ${{ github.workspace }}
              source activate-env.sh
              bitbake core-image-full-cmdline 2>&1 | tee build-log.txt
          "

      - name: Upload Build Log
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: yocto-build-log
          path: build-log.txt

      - name: Upload Build Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: yocto-build
          path: build/tmp/deploy/images/

