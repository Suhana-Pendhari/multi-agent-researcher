from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
    extract_text,
    clip_text,
    invoke_with_retry,
)

def run_research_pipline(topic:str)->dict:

    state = {}

    #search agent working
    print("\n" + "="*50)
    print("Step 1/4: Search Agent is working...")
    print("="*50)

    try:
        search_agent = build_search_agent()
        search_result = invoke_with_retry(search_agent, {
            "messages": [{"role": "user", "content": f"Find recent, reliable and detailed information about: {topic}"}]
        })
        state["search_results"] = extract_text(search_result)
        print("\n✅ Search completed!")
        print(f"Found {len(state['search_results'])} characters of search results")
    except Exception as e:
        print(f"\n❌ Error in search step: {str(e)}")
        return state

    #step2 - reader agent
    print("\n" + "="*50)
    print("Step 2/4: Reader Agent is scraping top resources...")
    print("="*50)

    try:
        reader_agent = build_reader_agent()
        reader_result = invoke_with_retry(reader_agent, {
            "messages": [{"role": "user", "content":
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{clip_text(state['search_results'], 900)}"
            }]
        })

        state['scraped_content'] = extract_text(reader_result)
        print("\n✅ Content scraping completed!")
        print(f"Scraped {len(state['scraped_content'])} characters of content")
    except Exception as e:
        print(f"\n❌ Error in reader step: {str(e)}")
        return state

    #step 3 - writer chain
    print("\n" + "="*50)
    print("Step 3/4: Writer is drafting the report...")
    print("="*50)

    try:
        research_combined = (
            f"SEARCH RESULTS:\n{clip_text(state['search_results'], 2200)}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{clip_text(state['scraped_content'], 2200)}"
        )

        if writer_chain is None:
            raise RuntimeError("Writer chain is not available because no LLM was initialized.")
        state['report'] = invoke_with_retry(writer_chain, {
            "topic": topic,
            "research": research_combined
        })

        print("\n✅ Report writing completed!")
        print(f"Generated {len(state['report'])} characters of report")
    except Exception as e:
        print(f"\n❌ Error in writer step: {str(e)}")
        return state

    #critic report
    print("\n" + "="*50)
    print("Step 4/4: Critic is reviewing the report...")
    print("="*50)

    try:
        if critic_chain is None:
            raise RuntimeError("Critic chain is not available because no LLM was initialized.")
        state['feedback'] = invoke_with_retry(critic_chain, {
            "report": clip_text(state['report'], 2800)
        })

        print("\n✅ Critique completed!")
        print(f"Generated {len(state['feedback'])} characters of feedback")
    except Exception as e:
        print(f"\n❌ Error in critic step: {str(e)}")
        return state

    print("\n" + "="*50)
    print("🎉 Pipeline completed successfully!")
    print("="*50)

    return state

if __name__ == "__main__":
    topic = input("\n Enter a research topic: ")
    run_research_pipline(topic)
    