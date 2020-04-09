mkdir build
cd build
conan install .. -u -s build_type=Debug -s compiler.runtime=MTd -s compiler.version=15 -r=conan-rtg --build missing
cmake -G "Visual Studio 15 Win64" .. 
cmake --build . --target mumlib --config Debug
cd ..
