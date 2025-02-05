#!/usr/bin/env node

import * as esbuild from 'esbuild'

esbuild
  .build({
    logLevel: "info",
    entryPoints: ['src/static/interface_check_password_leak.js'],
    bundle: true,
    outfile: 'src/static/index.bundle.js',
  })
  .catch(() => process.exit(1));

esbuild
  .build({
    logLevel: "info",
    entryPoints: ['src/static/interface_password_generation.js'],
    bundle: true,
    outfile: 'src/static/password_generation.bundle.js',
  })
  .catch(() => process.exit(1));

