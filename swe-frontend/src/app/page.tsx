import Image from "next/image";
import ReactMarkdown from 'react-markdown';

export default function Home() {
  const markdown = `
        # Hello, Markdown!
        
        This is a paragraph with *emphasis* and **strong importance**.
        
        - List item 1
        - List item 2
      `;


  return (
    <div className="flex items-center justify-center h-screen w-screen">
      <main className="w-4/5 h-7/8">
        {/* Header */}
        <div className="flex flex-row justify-center items-center">
          <div className="bg-gray-400 grow h-0.5 mr-4 rounded-md"></div>
          <div className="text-4xl flex-none font-exo">
            SWE-agent
          </div>
          <div className="bg-gray-400 grow h-0.5 ml-4 rounded-md"></div>
        </div>
        <div className="text-lg font-exo">
          v1
        </div>
        <div className="bg-gray-400 grow h-0.5 mt-4 rounded-md"></div>
        {/* Information */}
        <div className="grid gap-4 grid-cols-2 grid-rows-2 grid-flow-col-dense h-4/5 p-4">
          {/* Workspace */}
          <div className="row-span-2 rounded-md h-full overflow-hidden">
            <div className="flex flex-row">
              <Image
                src="/images/workspace.png"
                alt="Workspace"
                height={20}
                width={25}
              />
              <div className="mx-4 font-exo">
                Workspace
              </div>
            </div>
            <div className="w-full h-full pt-2">
              <div className="bg-white w-full h-full rounded-md text-black p-4 font-exo text-wrap">
                <ReactMarkdown>
                  {markdown}

                </ReactMarkdown>
              </div>
            </div>
          </div>
          {/* Terminal */}
          <div className=" rounded-md h-full overflow-hidden">
            <div className="flex flex-row">
              <Image
                src="/images/editor.png"
                alt="Editor"
                height={20}
                width={25}
              />
              <div className="mx-4 font-exo">
                Editor
              </div>
            </div>
            <div className="w-full h-full pt-2">
              <div className="bg-white w-full h-full rounded-md p-4 text-black font-exo">
                Editor holding text
              </div>
            </div>
          </div>
          {/* Editor */}
          <div className=" rounded-md h-full overflow-hidden">
            <div className="flex flex-row">
              <Image
                src="/images/terminal.png"
                alt="Terminal"
                height={20}
                width={25}
              />
              <div className="mx-4 font-exo">
                Terminal
              </div>
            </div>
            <div className="w-full h-full pt-2">
              <div className="bg-white w-full h-full rounded-md font-exo text-black p-4">
                temp terminal text
              </div>
            </div>
          </div>
        </div>
        <div className="flex flex-row w-full justify-around items-center font-exo">

          <div>
            Reset
          </div>

          <div>
            Next Step
          </div>
        </div>
        <div className="bg-gray-400 grow h-0.5 mt-4 rounded-md"></div>
        <div className="flex w-full justify-center items-center m-4 font-exo">
          Created by Basil Khwaja
        </div>
      </main>

    </div>
  );
}
