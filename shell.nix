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
    ];

    shellHook = ''
        # Set up a virtual environment if it doesn't exist
        if [ ! -d "venv" ]; then
        virtualenv venv
        fi
        source venv/bin/activate
        export PYTHONPATH=$PYTHONPATH:$(pwd)

        # Aliases
        alias run='python main.py'
        alias cls='clear'
    '';

    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
        pkgs.SDL2
        pkgs.SDL2_mixer
        pkgs.SDL2_image
        pkgs.SDL2_ttf
    ];
}