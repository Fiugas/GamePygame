{ pkgs ? import <nixpkgs> {} }:

let
    pythonEnv = pkgs.python3.withPackages (ps: with ps; [
        pygame
        moderngl
        numpy
    ]);
in
pkgs.mkShell {
    buildInputs = with pkgs; [
        pythonEnv
        SDL2
        SDL2_mixer
        SDL2_image
        SDL2_ttf
        python3Packages.pip
        python3Packages.virtualenv
        xorg.libX11
        xorg.libXi
        xorg.libXrandr
        libGL
        libGLU
        mesa
        libepoxy
        tree
    ];

    shellHook = ''
        export PYGAME_DETECT_AVX2=1
        export PYTHONPATH=$PYTHONPATH:$(pwd)

        # Virtual Environment
        if [ ! -d ".venv" ]; then
            echo "Creating virtual environment..."
            python -m venv .venv
        fi

        # Activate virtual environment
        source .venv/bin/activate

        # Aliases
        alias run='python game.py'
        alias cls='clear'
    '';

    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
        pkgs.SDL2
        pkgs.SDL2_mixer
        pkgs.SDL2_image
        pkgs.SDL2_ttf
        pkgs.libGL
        pkgs.libGLU
        pkgs.mesa
        pkgs.libepoxy
    ];
}